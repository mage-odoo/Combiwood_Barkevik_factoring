from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    assignment_clause = fields.Html(
        string="Assignment Clause", related='company_id.assignment_clause', readonly=False)
    partner_id = fields.Many2one(
        'res.partner', string='partner_account_id', related='company_id.partner_id', readonly=False)
