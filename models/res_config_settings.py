from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    assignment_clause = fields.Html(
        string="Assignment Clause", related='company_id.assignment_clause', readonly=False)
    factoring_partner_id = fields.Many2one(
        'res.partner', string='Factoring Partner', related='company_id.partner_id', readonly=False)
