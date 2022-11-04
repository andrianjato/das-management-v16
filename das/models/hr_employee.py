# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrResource(models.Model):
    _inherit = 'hr.employee'

    planning_ids = fields.One2many('das.planning', inverse_name='resource_id', string="Plannings")
    planning_count = fields.Integer(string="Planning count", compute='_compute_count_planning')


    @api.depends('planning_ids')
    def _compute_count_planning(self):
        for resource in self:
            resource.planning_count = len(resource.planning_ids)

    def get_resource_planning(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'das.planning',
            'domain': [('resource_id', '=', self.id)],
            'context': {'default_resource_id': self.id},
            'view_mode': 'gantt,tree',
            'target': 'current',
            'name': 'Plannings',
            'views': [
                (self.env.ref('das.view_das_planning_planning_gantt').id, 'gantt'),
                (self.env.ref('das.view_das_planning_planning_tree').id, 'tree')
            ]
        }

