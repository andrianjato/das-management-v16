# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = "project.task"

    total_hours = fields.Float(string='Total hours plannified', compute='_compute_total_hours')

    @api.depends('name')
    def _compute_total_hours(self):
        for rec in self:
            rec.total_hours = sum(
                self.env['das.planning'].search([('task_id.name', '=', rec.name)]).mapped('total_hours'))
