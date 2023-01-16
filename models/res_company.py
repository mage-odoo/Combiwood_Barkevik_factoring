from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    assignment_clause = fields.Html(
        string="Assignment Clause")
    factoring_partner_id = fields.Many2one(
        'res.partner', string='Factoring Partner', help="Factoring Partner")
