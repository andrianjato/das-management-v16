# -*- coding: utf-8 -*-

from odoo import models, fields


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    code_cc = fields.Char(string='Code CC')


