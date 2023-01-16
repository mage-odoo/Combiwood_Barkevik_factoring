from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_factoring = fields.Boolean(
        string='Is Factoring', help='the invoices to this customer will be default sold to the bank')
    factoring_partner = fields.Boolean(
        string="Factoring Partner", help='partner contact the invoices are sold to the bank')
