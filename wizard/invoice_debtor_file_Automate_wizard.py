import json
from odoo import models
from odoo import models, fields, api
from ..report import invoice_report as invo
import xlsxwriter


class invoice(models.TransientModel):
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
    def test_cron_job(self):
        workbook = xlsxwriter.Workbook('hello.excel')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Hello..')
        workbook.close()
        # data = {
        #     'name': 'manthan',
        #     'name1': 'manthan'
        # }
        # return {
        #     'type': 'ir.actions.report',
        #     'data': {
        #         'model': 'invoice.automate',
        #         'options': json.dumps(data, default=data_utils.json_default()),
        #         'output_format': 'xlsx',
        #         'report_name': 'xlsxreportexample'
        #     },
        #     'report_type': 'xlsx'
        # }


class debtor(models.TransientModel):
    _name = "debtor.info.automate"
    _description = "Debtor information send data at specific time"
    Transaction_code = fields.Char(size=1, help='1 for invoice', required=True)
    version_no = fields.Char(size=1, help='version number', required=True)
    client_no = fields.Char(size=1, help='Client Number', required=True)
    debtor_no = fields.Char(size=1, help='Debtor Number', required=True)
    org_no = fields.Char(
        size=1, help='Norwegian organization number', required=True)
    companyname = fields.Text(help='Company Name or last name', required=True)
    first_name = fields.Text(help='customer first name')
    postal_address = fields.Text(help='customer address', required=True)
    zip_code = fields.Char(help='zip code', required=True)
    city = fields.Text(help='customer city or town', required=True)
    reference = fields.Text(help='reference name')
    phone_no = fields.Text(help='Phone Number', required=True)
    country = fields.Text(help='Country name')
    country_code_alpha = fields.Text(help='Country code Alphabet')
    country_code_num = fields.Char(help='Country code Number', required=True)
    bank_acc_no = fields.Char(
        help='Debtors bank account number')
    seller_no = fields.Char(help='seller Number')
    name2 = fields.Text(help='Another Name')
    foreign_exchange_code = fields.Text(help='SEK,EUR,GBP,INR,USD')

    @api.model
    def run_cron_job(self):
        print("its run debtor")
