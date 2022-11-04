# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DasCategory(models.Model):
    _name = 'das.category'
    _description = 'Object for create new project category'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'category_project'

    category_project = fields.Char(string="Project category", required=True, tracking=True)
    type_id = fields.Many2one('das.category.type', string="Type", tracking=True)
    color = fields.Integer("Color", tracking=True)

    # For smart button
    account_ids = fields.One2many('das.account', 'category_id', string="Accounts")
    account_count = fields.Integer(string="Account count", compute='_compute_account_count')

    @api.depends('account_ids')
    def _compute_account_count(self):
        for category in self:
            category.account_count = len(category.account_ids)

    def get_category_account(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'das.account',
            'domain': [('category_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'name': 'Accounts',
            'views': [
                (self.env.ref('das.view_das_planning_account_tree').id, 'tree'),
                (self.env.ref('das.view_das_planning_account_form').id, 'form')
            ]
        }

    _sql_constraints = [
        ('name_uniq', 'unique (category_project)', "Tag name already exists!"), ]

