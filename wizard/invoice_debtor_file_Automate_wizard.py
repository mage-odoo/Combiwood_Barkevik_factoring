import json
from odoo import models
from odoo import models, fields, api


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
