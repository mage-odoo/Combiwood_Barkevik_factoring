from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    is_factoring = fields.Boolean(
        string='Is Factoring', tracking=True, help='the invoices to this customer will be default sold to the bank')
    factoring_partner = fields.Boolean(
        string="Factoring Partner",  tracking=True, help='partner contact the invoices are sold to the bank')
    # commercial_partner_id_temp = fields.

    @api.onchange('factoring_partner')
    def _onchange_factoring_partner(self):
        print(self.factoring_partner)
