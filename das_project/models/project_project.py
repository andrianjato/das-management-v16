# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class ProjectProject(models.Model):
    _name = 'project.project'
    _inherit = ['project.project', 'mail.thread', 'mail.activity.mixin']

    key = fields.Char(string="Project key", tracking=True)
    name = fields.Char(tracking=True)
    label_tasks = fields.Char(tracking=True)
    description = fields.Html(tracking=True)
    user_id = fields.Many2one(tracking=True)
    partner_id = fields.Many2one(tracking=True)
    partner_phone = fields.Char(tracking=True)
    partner_email = fields.Char(tracking=True)
    privacy_visibility = fields.Selection(tracking=True)
    allowed_portal_user_ids = fields.Many2many(tracking=True)

    # total_days = fields.Float(string='Total days plannified', compute='_compute_total_hours')
    # remaining_days = fields.Float(string='Remaining day', compute='_compute_total_hours')
    # percentage_days = fields.Float(string='Percentage', compute='_compute_total_hours')
    #
    # @api.depends('name', 'date_start', 'date')
    # def _compute_total_hours(self):
    #     for rec in self:
    #         # count total days plannified
    #         rec.total_days = (sum(
    #             self.env['das.planning'].search([('project_id.name', '=', rec.name)]).mapped('total_hours'))) / 8
    #
    #         day = rec.date_start
    #         day_counter = 0
    #         if rec.date:
    #             while day <= rec.date:
    #                 if day.weekday() < 5:
    #                     day_counter += 1
    #                 day += timedelta(days=1)
    #         if not day_counter:
    #             rec.percentage_days = 0
    #             rec.remaining_days = day_counter - rec.total_days
    #         else:
    #             rec.remaining_days = day_counter - rec.total_days
    #             rec.percentage_days = rec.total_days * 100 / day_counter
