# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError


class DasPlanning(models.Model):
    _name = 'das.planning'
    _description = "DAS Planning"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'account_label'

    resource_id = fields.Many2one('hr.employee', string="Resource", required=True, tracking=True)
    resource_id_active = fields.Boolean('hr.employee', related='resource_id.active',
                                        store=True)
    resource_departure_date = fields.Date(string="Departure date", related='resource_id.departure_date')
    resource_departure_reason_id = fields.Many2one(string="Departure reason", related='resource_id.departure_reason_id')

    account_id = fields.Many2one('das.account', string="Account", required=True, tracking=True)
    start_date = fields.Date(string="Start date", default=fields.Date.today, required=True, tracking=True)
    end_date = fields.Date(string="End date", default=fields.Date.today, required=True, tracking=True)
    date_delta = fields.Integer(string="Number of days beetwen two dates", compute='_compute_date_delta', store=True)
    daily_hours = fields.Integer(string="Daily hours", default=8, tracking=True)
    total_hours = fields.Integer(string="Total hours", compute='_calculate_total_hours', store=True, readonly=True)
    account_label = fields.Char(string="Account label", compute='_compute_account_label', readonly=True)
    active = fields.Boolean(string="Active", default=True, tracking=True)

    department_id = fields.Many2one('hr.department', related='resource_id.department_id', store=True)
    type_id = fields.Many2one(related='account_id.type_id', string="Type", store=True)
    job = fields.Char(related='resource_id.job_id.name', string="Job", store=True)
    resource_reference = fields.Char(related='resource_id.reference', string="Resource reference", store=True)
    color = fields.Integer(related='account_id.category_id.color', store=True)
    planning_date = fields.One2many('das.planning.date', inverse_name='planning_id', string="Date Planning")

    project_id = fields.Many2one('project.project', string='Project', related='account_id.project_id', readonly="True")
    task_id = fields.Many2one('project.task', string='Task', tracking=True)

    globals_leaves_ids = fields.One2many(string="Global leave of current month",
                                         related='resource_id.resource_calendar_id.global_leave_ids')

    @api.onchange("project_id")
    def _set_project_domains(self):
        """Filter task and account based on project """
        if self.project_id:
            return {
                'domain': {
                    'task_id': [('project_id', '=', self.project_id.id)],
                    'account_id': [('project_id', '=', self.project_id.id)]
                }
            }

    @api.depends('resource_id', 'daily_hours', 'account_id')
    def _compute_account_label(self):
        """Add daily hours in account reference to show in planning Gantt view"""
        for planning in self:
            planning.account_label = str(planning.daily_hours) + " h/j " + str(planning.account_id.key)

    @api.depends('daily_hours', 'start_date', 'end_date')
    def _calculate_total_hours(self):
        for planning in self:
            if planning.start_date:
                day = planning.start_date
                days_counter = 0
                while day <= planning.end_date:
                    if day.weekday() < 5:
                        days_counter += 1
                    day += timedelta(days=1)
                planning.total_hours = planning.daily_hours * days_counter

    @api.depends('start_date', 'end_date')
    def _compute_date_delta(self):
        for planning in self:
            planning.date_delta = (planning.end_date - planning.start_date).days + 1

    @api.onchange('daily_hours')
    def _check_daily_hours(self):
        """Check immediately (onchange) a valid daily working hours"""
        for planning in self:
            if not 0 <= planning.daily_hours <= 8:
                planning.daily_hours = 8
                return {'warning': {
                    'title': 'Value Error',
                    'message': _("Sorry, Daily working hours is between 0 to 8 !"),
                }}

    @api.onchange('resource_id', 'start_date', 'end_date', 'daily_hours')
    def _check_planning_existence(self):
        date = self.start_date
        if date:
            total_daily_hours = []
            while date <= self.end_date:
                days_planning_hours = self.env['das.planning'].search(
                    [('resource_id', '=', self.resource_id.id), ('id', '!=', self._origin.id)]).filtered(
                    lambda p: p.start_date <= date <= p.end_date).mapped('daily_hours')
                total_daily_hours.append(sum(days_planning_hours))
                date += timedelta(days=1)

            for planning in self:
                new_hour_limit = 8 - max(total_daily_hours)
                if not 0 <= planning.daily_hours <= new_hour_limit:
                    planning.daily_hours = new_hour_limit
                    return {'warning': {
                        'title': 'Attention',
                        'message': _("Remaining working hours : " + str(new_hour_limit) + " h"),
                    }}

    @api.constrains('resource_id', 'daily_hours', 'start_date', 'end_date')
    def _check_resource_daily_hours(self):
        resource_plannings = self.env['das.planning'].search(
            [('resource_id', '=', self.resource_id.id), ('account_id.type_id.is_no_counting', '!=', True)])
        planning_min_date = min(resource_plannings.mapped('start_date'))
        planning_max_date = max(resource_plannings.mapped('end_date'))
        date = planning_min_date
        while date <= planning_max_date:
            planning_days_hours = resource_plannings.filtered(lambda p: p.start_date <= date <= p.end_date).mapped(
                'daily_hours')
            if sum(planning_days_hours) > 8:
                raise ValidationError(_('Daily working hours must be inferior to 8 !'))
            date += timedelta(days=1)

    def create_planning_date(self):
        date = self.start_date
        while date <= self.end_date:
            leaves = self.env['resource.calendar.leaves'].search([]).filtered(
                lambda l: l.date_from.date() <= date <= l.date_to.date())
            if date.weekday() < 5 and not leaves:
                self.env['das.planning.date'].sudo().create({
                    'date': date,
                    'planning_id': self.id
                })
            date += timedelta(days=1)

    @api.model
    def create(self, vals):
        res = super(DasPlanning, self).create(vals)
        res.create_planning_date()
        return res

    def write(self, vals):
        # Modify Das planning per date if das planning model changed
        res = super(DasPlanning, self).write(vals)
        for planning in self:
            self.env['das.planning.date'].sudo().search([('planning_id', '=', planning.id)]).unlink()
            if planning.active:
                planning.create_planning_date()
        return res

    @api.model
    def gantt_unavailability(self, start_date, end_date, scale, group_bys=None, rows=None):
        """ Color weekends and leaves to Grey"""

        if scale != "year":
            local_format = "%Y-%m-%d %H:%M:%S"
            unavailabilities = []

            # Grey Weekends
            date = datetime.strptime(start_date, local_format)
            while date <= datetime.strptime(end_date, local_format):
                if date.weekday() == 5:
                    start = date.replace(hour=0, minute=0, second=0) - timedelta(hours=3)
                    stop = (date + timedelta(days=1)).replace(hour=23, minute=59, second=59) - timedelta(hours=3)
                    unavailabilities.append(
                        {'start': start.strftime(local_format), 'stop': stop.strftime(local_format)})
                date += timedelta(days=1)

            # Grey HR leaves
            leaves = self.env['resource.calendar.leaves'].search([])
            for leave in leaves:
                start = leave.date_from.replace(hour=0, minute=0, second=0) - timedelta(hours=3)
                stop = leave.date_to.replace(hour=23, minute=59, second=59) - timedelta(hours=3)
                unavailabilities.append(
                    {'start': start.strftime(local_format), 'stop': stop.strftime(local_format)})

            sorted_unavailabilities = sorted(unavailabilities, key=lambda d: d['start'])
            for row in rows:
                row['unavailabilities'] = sorted_unavailabilities

        return rows
