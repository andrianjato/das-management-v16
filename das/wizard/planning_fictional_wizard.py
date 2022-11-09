# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError


class PlanningFictionalWizard(models.TransientModel):
    _name = 'planning.fictional.wizard'
    _description = "Generate Planning fictional on Wizard"

    batch_id = fields.Many2one('das.fictional.batch', string='Batch name')
    start_date = fields.Date(string='Start date', related='batch_id.start_date', readonly=True)
    end_date = fields.Date(string='End date', related='batch_id.end_date', readonly=True)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    resource_ids = fields.Many2many('hr.employee', string="Job", required=True)

    @api.onchange("department_id")
    def _set_resource_ids_domains(self):
        """Filter resource based on department """
        if self.department_id:
            return {
                'domain': {
                    'resource_ids': [('department_id', '=', self.department_id.id), ('active', '=', True)],
                }
            }

    @api.depends('date', 'resource_ids', 'planning_id')
    def generate_fictional_planning(self):
        """ This function  help user to generate monthly fictional planning for all resources"""
        planing_date = self.env['das.planning.date'].search([])
        resource_id = self.env['hr.employee']
        date_planned = set(planing_date.search([('date', '>=', self.start_date)]).mapped('date'))
        date_from = self.start_date
        date_to = self.end_date
        date_list = []
        while date_from <= date_to:
            if date_from.weekday() < 5 and date_from not in date_planned:
                date_list.append(date_from)
            date_from += timedelta(days=1)

        account_id = self.env['das.account'].sudo().search(
            [('reference', '=', '[fic_project] Fictional project [Fic Account ref]')]).id
        for res in self.resource_ids.mapped('id'):
            for date_to_plan in date_list:
                if not planing_date.search(
                        [('resource_id', '=', resource_id.browse(res).id), ('date', '=', date_to_plan),
                         ('account_id', '=', account_id)]):
                    total_daily_hours = sum(self.env['das.planning.date'].search(
                        [('resource_id', '=', resource_id.browse(res).id), ('date', '=', date_to_plan)]).mapped(
                        'daily_hours'))
                    self.env['das.planning'].sudo().create(
                        {'resource_id': resource_id.browse(res).id,
                         'account_id': account_id,
                         'daily_hours': 8 - total_daily_hours,
                         'start_date': date_to_plan, 'end_date': date_to_plan})
