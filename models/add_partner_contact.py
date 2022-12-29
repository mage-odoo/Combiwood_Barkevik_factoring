from odoo import models, fields, api
from ..wizard import sale_advance_payment_inv_wizard as tem


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

    is_factoring = fields.Boolean(
        string='is_factoring', compute='_onchange_is_factoring', store=True)

    # def getdata(self):
    #     fetchdata = self.env[sale.order].search([])

    @api.depends('invoice_user_id')
    def _onchange_is_factoring(self):
        if tem.temp.t1 != 2:
            for rec in self:
                rec.is_factoring = tem.temp.t1
                return self
        tem.temp.t1 = 2
        print(tem.temp.t1)

    # def default_get(self, fields):
    #     res = super(AddAccountMove, self).default_get(fields)
    #     # res.update({
    #     #     'is_factoring': self.env['sale.advance.payment.inv'].is_factoring_temp
    #     # })

    #     return res


class bankaccountisfectoring(models.Model):
    _inherit = "res.partner.bank"
    is_factoring = fields.Boolean(string='Is Factoring', default=1)
