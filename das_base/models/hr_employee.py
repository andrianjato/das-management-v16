# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrResource(models.Model):
    _inherit = 'hr.employee'

    reference = fields.Char(string="Reference", compute="_compute_reference", store=True)
    appelation = fields.Char(string="Appelation", default=" ")
    registration_number = fields.Integer(string="Registration number", default=0)

    # ------ get reference automatically ----- #
    @api.depends('registration_number', 'appelation', 'job_id')
    def _compute_reference(self):
        for rec in self:
            if not rec.job_id or not rec.registration_number or not rec.appelation:
                rec.reference = " "
            else:
                rec.reference = str(rec.registration_number) + " - " + str(rec.appelation) + " (" + str(
                    rec.job_id.display_name) + ")"

    def name_get(self):
        result = []
        for record in self:
            name = record.reference
            result.append((record.id, name))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        domain = [
                     ('reference', operator, name)
                 ] + (args or [])
        recs = self.search(domain, limit=limit)
        return recs.name_get()
