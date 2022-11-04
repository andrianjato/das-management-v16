# -*- coding: utf-8 -*-

from odoo import models, fields


class HrJobType(models.Model):
    _name = 'hr.job.type'
    _description = "Hr Job Type"
    _rec_name = 'type'

    type = fields.Char(string="Type", required=True)
    description = fields.Text(string="Description")
