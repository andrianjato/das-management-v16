# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    account_ids = fields.One2many('das.account', 'project_id', string="Accounts")
    account_count = fields.Integer(string="Account", compute='_compute_account_count')

    def get_project_account(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'das.account',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
            'view_mode': 'tree',
            'target': 'current',
            'name': 'Accounts',
            'views': [
                (self.env.ref('das.view_das_planning_account_tree').id, 'tree'),
                (self.env.ref('das.view_das_planning_account_form').id, 'form')
            ]
        }

    @api.depends('account_ids')
    def _compute_account_count(self):
        for project in self:
            project.account_count = len(project.account_ids)
