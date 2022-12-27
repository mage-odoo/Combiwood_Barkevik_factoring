from odoo import models, fields, api


class AddPartnerContact(models.Model):
    _inherit = "res.partner"
    is_factoring = fields.Boolean(
        string='Is Factoring',  help='the invoices to this customer will be default sold to the bank', default=0)
    factoring_partner = fields.Boolean(
        string="Factoring Partner",  help='partner contact the invoices are sold to the bank')


class AddSalesOrder(models.Model):
    _inherit = "sale.order"
    is_factoring = fields.Boolean(string='Is Factoring', tracking=True)

    @api.onchange('partner_id')
    def _onchange_is_factoring(self):
        self.is_factoring = self.partner_id.is_factoring


class AddAccountMove(models.Model):
    _inherit = "account.move"
    is_factorial_id = fields.Many2one('sale.order')
    is_factoring = fields.Boolean(store=True,
                                  related='is_factorial_id.is_factoring')
