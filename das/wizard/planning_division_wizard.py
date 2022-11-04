# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError
from lxml import etree


class PlanningDivisionWizard(models.TransientModel):
    _name = 'planning.division.wizard'
    _description = "Planning Division Wizard"

    planning_id = fields.Many2one('das.planning', string="Planning", readonly=True)
    start_date = fields.Date(string="Start date", required=True)
    end_date = fields.Date(string="End date", required=True)
    new_account_id = fields.Many2one('das.account', string="New Account", required=True)

    @api.model
    def default_get(self, fields):
        res = super(PlanningDivisionWizard, self).default_get(fields)
        planning_active = self._context.get('active_id')
        res.update({'planning_id': planning_active})
        return res

    def divide_planning(self):
        planning = self.planning_id
        end = planning.end_date
        self.planning_id.write({'end_date': self.start_date - timedelta(days=1)})
        planning.copy({'start_date': self.start_date, 'end_date': self.end_date, 'account_id': self.new_account_id.id})
        planning.copy({'start_date': self.end_date + timedelta(days=1), 'end_date': end})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'das.planning',
            'domain': [],
            'view_mode': 'gantt,calendar,tree,form',
            'target': 'current',
            'name': 'Division',
            'views': [
                (self.env.ref('das.view_das_planning_planning_gantt').id, 'gantt'),
                (self.env.ref('das.view_das_planning_planning_tree').id, 'tree'),
                (self.env.ref('das.view_das_planning_planning_form').id, 'form')
            ]
        }

    @api.constrains('start_date')
    def _check_start_date(self):
        for rec in self:
            start_date = rec.planning_id.start_date
            if rec.start_date < start_date:
                raise ValidationError("Start date must be superior to " + str(start_date))

    @api.constrains('end_date')
    def _check_end_date(self):
        for rec in self:
            end_date = rec.planning_id.end_date
            if rec.end_date > end_date:
                raise ValidationError("End date must be inferior to " + str(end_date))

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(PlanningDivisionWizard, self).fields_view_get(view_id=view_id, view_type=view_type,
                                                                     toolbar=toolbar, submenu=submenu)

        if view_type == 'form':
            doc = etree.XML(result['arch'])
            start_date = doc.xpath("//field[@name='start_date']")
            end_date = doc.xpath("//field[@name='end_date']")

            if start_date and end_date:
                planning = self.env['das.planning'].browse(self.env.context.get('active_id'))
                option = '{"datepicker": {"daysOfWeekDisabled": [0, 6], ' \
                         '"minDate": "' + str(planning.start_date) + \
                         '", "maxDate": "' + str(planning.end_date) + '"}}'

                start_date[0].set("options", option)
                end_date[0].set("options", option)
                result['arch'] = etree.tostring(doc, encoding='unicode')
        return result
