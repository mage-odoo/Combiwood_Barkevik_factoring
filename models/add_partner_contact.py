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


class advance_payment_inv_inherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    is_factoring_temp = fields.Boolean(string='Is Factoring')

    def create_invoices(self):
        print("done calling.............................")
        super(advance_payment_inv_inherit, self).create_invoices()


class AddAccountMove(models.Model):
    _inherit = "account.move"
    is_factorial_id = fields.Many2one('sale.order')
    is_factoring = fields.Char(store=True)


class ressetting(models.TransientModel):
    _inherit = "res.config.settings"
    is_factoring = fields.Boolean(string='Is Factoring', default=1)


class bankaccountisfectoring(models.Model):
    _inherit = "res.partner.bank"
    is_factoring = fields.Boolean(string='Is Factoring', default=1)
