from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'
    assignment_clause = fields.Html(
        string="Assignment Clause", default="test data")
    partner_id = fields.Many2one(
        'res.partner', string='partner_account_id', help="Factoring Partner")
