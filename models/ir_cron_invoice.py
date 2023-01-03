from odoo import models, fields, api


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

    @ api.model
    def run_cron_job(self):
        print("called")
        return self.env.ref('Combiwood_Barkevik_factoring.report_invoice_report_data_xlsx').report_action(self)
