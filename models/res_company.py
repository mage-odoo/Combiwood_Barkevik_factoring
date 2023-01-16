from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    assignment_clause = fields.Html(
        string="Assignment Clause")
    partner_id = fields.Many2one(
        'res.partner', string='Partner Account Id', help="Factoring Partner")
