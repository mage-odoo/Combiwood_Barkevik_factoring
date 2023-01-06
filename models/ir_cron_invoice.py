from odoo import models, fields, api
from datetime import timedelta
import os


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

    def run_cron_job(self):
        print("called")
        notificcation_date = fields.datetime.today().today() - timedelta(days=1)
        notificcation_date = notificcation_date.replace(
            minute=31, hour=15, second=0, microsecond=0)
        today_date = fields.datetime.today().replace(
            minute=30, hour=15, second=0, microsecond=0)
        # for i in self.env['account.move'].search(['&', '&', ('create_date', '>', notificcation_date), ('create_date', '<=', today_date), ('name', '!=', '/')]):
        #     print(i.create_date)
        #     print(i.amount_total_signed)
        path = "/home/odoo/dev/"
        file_name = "/faktura.sgf"
        folder_date = str(fields.date.today())
        path = path+folder_date
        try:
            os.mkdir(path, mode=511)
            final_path = path+file_name
            open(final_path, "w").close()
            f = open(final_path, "a", encoding="utf-16")
            for i in self.env['account.move'].search(['&', '&', '&', ('name', '!=', '/'),  ('name', '!=', 'PBNK*'), ('create_date', '>', notificcation_date), ('create_date', '<', today_date)]):
                if i.name[0:4] != 'PBNK':
                    # print(i.create_date)
                    a = "Invoice " if i.name[0:4] == 'INV/' else "Credit note "
                    f.write(str(1 if i.name[0:4] == 'INV/' else 9)+" ")
                    payment_reference = (
                        '0' * (4-int(len(str(i.payment_reference))))) + str(i.payment_reference)
                    f.write(payment_reference[:4]+" ")
                    customer_id = (
                        '0' * (9-int(len(str(i.partner_id.id)))))+str(i.partner_id.id)
                    f.write(customer_id+" ")
                    credit_note_number = str(i.name).split("/")[2]
                    final_credit_note_number = (
                        ('0' * (8-int(len(str(credit_note_number))))))+str(credit_note_number)
                    f.write(final_credit_note_number+" ")
                    f.write((i.invoice_date).strftime("%y%m%d")+" ")
                    f.write((i.invoice_date_due).strftime("%y%m%d")+" ")
                    Amount_total_signed = (
                        '0' * (11-int(len(str(i.amount_total_signed))))) + str(abs(i.amount_total_signed))
                    f.write(Amount_total_signed+" ")
                    creation_date = (i.create_date).date()
                    last_discount_date = (i.create_date).date() + \
                        timedelta(days=10)
                    print("invoce ", i.invoice_date)
                    print(creation_date)
                    print(last_discount_date)
                    if (creation_date >= (i.invoice_date) and (i.invoice_date) <= last_discount_date):
                        f.write('Allow for discount')
                    f.write("\n")
            f.close()

            with open(final_path, "r", encoding="utf-16") as myfile:
                print(myfile.read())
        except FileExistsError:
            print("file already presenr")
