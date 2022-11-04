# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta
import calendar


# use name_get not _rec_name ( error in resource.resource)
class HrResource(models.Model):
    _inherit = 'hr.employee'

    first_name = fields.Char(string="First name")
    login_jira = fields.Char(string="Jira login")
    name_jira = fields.Char(string="Jira name")
    ref_name = fields.Char(string="Ref name", compute="_compute_ref_name", store=True)
    previous_department_id = fields.Many2one('hr.department')
    department_id = fields.Many2one('hr.department')
    code_cc = fields.Char(related="department_id.code_cc", store=True)
    # dates_not_planned = fields.Char(string='Date not planned', compute='_compute_dates_not_planned')
    total_resource = fields.Integer(string="Total resource", default=lambda self: self.get_total_resource())

    @api.depends('code_cc', 'appelation', 'job_id')
    def _compute_ref_name(self):
        for rec in self:
            if not rec.code_cc or not rec.appelation or not rec.job_id:
                rec.ref_name = " "
            else:
                rec.ref_name = "[" + str(rec.code_cc) + "] " + str(rec.appelation) + " (" + str(
                    rec.job_id.display_name) + ")"

    def _compute_dates_not_planned(self):
        for rec in self:
            today = datetime.today()
            last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
            date_liste = []
            date_liste_not_planned = []
            planning = self.env['das.planning.date'].sudo().search(
                [('resource_id', '=', self.id)])

            while today <= last_day:
                date_liste.append(today.date())
                today += timedelta(days=1)

            date_planned = []
            for p in planning:
                date_planned.append(str(p.date))

            for d in date_liste:
                if str(d) not in date_planned and d.weekday() < 5:
                    date_liste_not_planned.append(str(d))
            rec.dates_not_planned = ' ; '.join(date_liste_not_planned)

    def get_total_resource(self):
        return self.env['hr.employee'].search_count([('active', '=', True)])

    def set_total_resource(self):
        obj_employee = self.env['hr.employee']
        resources = obj_employee.search([]) + obj_employee.search([('active', '=', False)])
        for resource in resources:
            resource.total_resource = self.get_total_resource()

    def toggle_active(self):
        res = super(HrResource, self).toggle_active()
        self.set_total_resource()
        return res

    @api.model
    def create(self, vals):
        res = super(HrResource, self).create(vals)
        self.set_total_resource()
        return res

    def unlink(self):
        res = super(HrResource, self).unlink()
        self.set_total_resource()
        return res
