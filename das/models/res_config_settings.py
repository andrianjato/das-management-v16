# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    billable_goal = fields.Integer(string="Billable goal", default=70)

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
        param.set_param('das.billable_goal', self.billable_goal)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(billable_goal=self.env['ir.config_parameter'].sudo().get_param('das.billable_goal'))
        return res

    @api.constrains('billable_goal')
    def _check_billable_goal(self):
        if self.billable_goal < 0 or self.billable_goal > 100:
            raise ValidationError(_('Purcentage must be between 0 and 100 !'))


