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
        string='is_factoring', store=True, default=lambda self: self.env['sale.advance.payment.inv'].search(['is_factoring_temp']).exists())

    # @api.depends('invoice_user_id', 'partner_id')
    # def _onchange_is_factoring(self):
    #     print("_onchange_is_factoring")
    #     if tem.temp.t1 != 2:
    #         for rec in self:
    #             rec.is_factoring = tem.temp.t1
    #             return self
    #     tem.temp.t1 = 2
    #     print(tem.temp.t1)

    @api.onchange('partner_id', 'invoice_user_id')
    def _onchange_is_factoring(self):
        print("onchange called")
        self.is_factoring = self.partner_id.is_factoring

    # # def getdata(self):
    # #     fetchdata = self.env[sale.order].search([])

    # def default_get(self, fields):
    #     res = super(AddAccountMove, self).default_get(fields)
    #     res.update({
    #         'is_factoring': self.env['sale.advance.payment.inv'].is_factoring_temp
    #     })

    #     return res


class bankaccountisfectoring(models.Model):
    _inherit = "res.partner.bank"
    is_factoring = fields.Boolean(string='Is Factoring', default=1)


class invoice(models.Model):
    _name = "invoice.automate"
    _description = "invoice model for send data at specific time"

    Transaction_code = fields.Char(size=1, help='1 for invoice', required=True)
    Client_no = fields.Char(
        help='Constant value notified by NFE', required=True)
    Customers_id = fields.Char(help='Debtor number', required=True)
    credit_note_no = fields.Char(help='Credit note no', required=True)
    credit_note_date = fields.Char(help='Formate YYMMDD', required=True)
    due_date = fields.Char(
        help='due is same as credit card note date', required=True)
    amount = fields.Char(help='Amount totel', required=True)
    discount_term = fields.Char(
        help='Invoice matching the credit note number', required=True)
    not_in_use = fields.Char(help='note in use')
    text_ordernr = fields.Text(help='Information to customer')
    text_comment = fields.Text(help='Comment on invoice')
    sellers_no = fields.Text(help='Clients sellers no')
    project_no = fields.Text(help='Clients Poject no')
    foreign_exchange_code = fields.Text(
        help='SEK,EUR,GBP,INR,USD')
    foreign_exchange_amount = fields.Text(
        help='Foreign exchange amount incl 2 decimal')

    @api.model
    def run_cron_job(self):
        print("called")
        return self.env.ref('Combiwood_Barkevik_factoring.report_invoice_report_data_xlsx').report_action(self)
