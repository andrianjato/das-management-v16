# -*- coding: utf-8 -*-

from odoo import models, fields


class HrJob(models.Model):
    _inherit = 'hr.job'

    type_id = fields.Many2one('hr.job.type', string="Type")
