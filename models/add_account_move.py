from odoo import models, fields, api


class AddAccountMove(models.Model):
    _inherit = "account.move"

    is_factoring = fields.Boolean(
        string='Is Factoring', readonly=True)
