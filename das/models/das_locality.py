# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DasLocality(models.Model):
    _name = 'das.locality'
    _description = "DAS Locality"
    _rec_name = "locality"

    locality = fields.Char(string="Locality", required=True)
    description = fields.Text(string="Description")

    # For smart button
    account_reference_ids = fields.One2many('das.account.reference', 'locality_id', string="Account reference")
    reference_account_count = fields.Integer(string="Account reference count",
                                             compute='_compute_reference_account_count')

    @api.depends('account_reference_ids')
    def _compute_reference_account_count(self):
        for locality in self:
            locality.reference_account_count = len(locality.account_reference_ids)

    def get_reference_account_locality(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'das.account.reference',
            'domain': [('locality_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
            'name': 'Locality',
            'views': [
                (self.env.ref('das.view_das_planning_locality_tree').id, 'tree'),
                (self.env.ref('das.view_das_planning_locality_form').id, 'form')
            ]
        }
