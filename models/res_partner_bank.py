from odoo import models, fields


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    is_factoring = fields.Boolean(
        string='Is Factoring', default=1)
