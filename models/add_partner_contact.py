from odoo import models, fields, api


class AddPartnerContact(models.Model):
    _inherit = "res.partner"

    is_factoring = fields.Boolean(string='Is Factoring')
    factoring_partner = fields.Boolean(string="Factoring Partner")
