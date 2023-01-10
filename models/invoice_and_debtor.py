from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import os


class InvoiceAndDebtor(models.Model):
    _name = "invoice.and.debtor"
    _description = "invoice and debtor for send data at specific time (Cron Job)"

    def run_cron_job(self):
        # invoice file
        notificcation_date = fields.datetime.today().today() - timedelta(days=1)
        notificcation_date = notificcation_date.replace(
            minute=31, hour=15, second=0, microsecond=0)
        today_date = fields.datetime.today().replace(
            minute=30, hour=15, second=0, microsecond=0)
        path = "/home/odoo/dev/"
        file_name = "/faktura.sgf"
        file_name2 = "/kunde.sgf"
        folder_date = str(fields.date.today())
        path = path+folder_date
        try:
            os.mkdir(path, mode=511)
            final_path = path+file_name
            open(final_path, "w").close()
            f = open(final_path, "a", encoding="utf-16")
            for i in self.env['account.move'].search(['&', '&', '&', ('name', '!=', '/'),  ('name', '!=', 'PBNK*'), ('create_date', '>', notificcation_date), ('create_date', '<', today_date)]):
                if i.name[0:4] != 'PBNK':
                    a = "Invoice " if i.name[0:4] == 'INV/' else "Credit note "
                    f.write(str(1 if i.name[0:4] == 'INV/' else 9))
                    payment_reference = (
                        '0' * (4-int(len(str(i.payment_reference))))) + str(i.payment_reference)
                    f.write(payment_reference[:4])
                    customer_id = (
                        '0' * (9-int(len(str(i.partner_id.id)))))+str(i.partner_id.id)
                    f.write(customer_id)
                    credit_note_number = str(i.name).split("/")[2]
                    final_credit_note_number = (
                        ('0' * (8-int(len(str(credit_note_number))))))+str(credit_note_number)
                    f.write(final_credit_note_number)
                    f.write((i.invoice_date).strftime("%y%m%d"))
                    f.write((i.invoice_date_due).strftime("%y%m%d"))
                    Amount_total_signed = (
                        '0' * (11-int(len(str(abs(i.amount_total_signed)))))) + str(abs(i.amount_total_signed))
                    f.write(Amount_total_signed)
                    creation_date = (i.create_date).date()
                    last_discount_date = (i.create_date).date() + \
                        timedelta(days=10)
                    finalvalue = ""
                    if i.name[0:3] == 'INV':
                        if (creation_date >= (i.invoice_date) and (i.invoice_date) <= last_discount_date):
                            if i.invoice_payment_term_id.line_ids.discount_percentage != '0.0':
                                # final_discount = (
                                #     ('0' * (8-int(len(str(i.))))))+str(credit_note_number)

                                finalvalue = "0"+str(i.invoice_payment_term_id.line_ids.discount_days) + \
                                    (str(i.invoice_payment_term_id.line_ids.discount_percentage).replace(
                                        ".", ""))
                                if int(finalvalue):
                                    f.write(finalvalue)
                    for rec in self.env['res.currency'].search([('active', '=', '1')]):
                        if finalvalue == "" or int(finalvalue) == 0:
                            f.write("     ")
                    f.write(" "*8)
                    f.write(" "*15)
                    f.write(" "*25)
                    f.write(" "*4)
                    f.write(" "*7)
                    f.write(rec.name)
                    f.write(" "*11)
                    f.write("\n")
            f.close()
            with open(final_path, "r", encoding="utf-16") as myfile:
                print(myfile.read())
                final_path = path+file_name

            # Debtor file
            final_path = path+file_name2
            open(final_path, "w").close()
            f = open(final_path, "a", encoding="utf-16")
            for rec in self.env['res.partner'].search([]):
                f.write("k")
                f.write("9409")
                f.write("1195")

                if len(str(rec.ref)) <= 9:
                    if type(rec.ref) == bool:
                        f.write(" "*9)
                    elif rec.ref == 9:
                        f.write(str(rec.ref))
                    else:
                        f.write(((' ' * (9-int(len(str(rec.ref))))))+str(rec.ref))
                else:
                    f.write(str(rec.ref)[:9])

                if len(str(rec.l10n_no_bronnoysund_number)) <= 11:
                    if type(rec.l10n_no_bronnoysund_number) == bool:
                        f.write(" "*11)
                    elif rec.l10n_no_bronnoysund_number == 11:
                        f.write(str(rec.l10n_no_bronnoysund_number))
                    else:
                        f.write(str(rec.l10n_no_bronnoysund_number)+((' ' *
                                (11-int(len(str(rec.l10n_no_bronnoysund_number)))))))
                else:
                    f.write(str(rec.l10n_no_bronnoysund_number)[:11])

                if len(str(rec.name)) <= 35:
                    if type(rec.name) == bool:
                        f.write(" "*35)
                    elif rec.name == 35:
                        f.write(str(rec.name))
                    else:
                        f.write(str(rec.name) +
                                ((' ' * (35-int(len(str(rec.name)))))))
                else:
                    f.write(str(rec.name)[:35])

                f.write(" "*20)

                if len(str(rec.street)) <= 30:
                    if type(rec.street) == bool:
                        f.write(" "*30)
                    elif rec.street == 30:
                        f.write(str(rec.street))
                    else:
                        f.write(str(rec.street) +
                                ((' ' * (30-int(len(str(rec.street)))))))
                else:
                    f.write(str(rec.street)[:30])

                if len(str(rec.zip)) <= 4:
                    if type(rec.zip) == bool:
                        f.write(" "*4)
                    elif rec.zip == 4:
                        f.write(str(rec.zip))
                    else:
                        f.write(str(rec.zip) +
                                ((' ' * (4-int(len(str(rec.zip)))))))
                else:
                    if type(rec.zip) == bool:
                        f.write(" "*4)
                    else:
                        f.write(str(rec.zip)[:4])

                if len(str(rec.city)) <= 23:
                    if type(rec.city) == bool:
                        f.write(" "*23)
                    elif rec.city == 23:
                        f.write(str(rec.city))
                    else:
                        f.write(str(rec.city) +
                                ((' ' * (23-int(len(str(rec.city)))))))
                else:
                    f.write(str(rec.city)[:23])

                f.write(" "*20)
                f.write(" "*12)
                f.write("Norge")
                f.write(" "*15)
                f.write("NO")
                f.write("578")
                f.write(" "*11)
                f.write(" "*4)
                f.write(" "*35)
                f.write("NOK")
                f.write("\n")
            f.close()
            with open(final_path, "r", encoding="utf-16") as myfile:
                print(myfile.read())
        except FileExistsError:
            raise ValidationError(
                "invoice.and.debtor model folder location {0} already file {1} And {2} are exist.\nDelete Folder {0}".format(path, file_name, file_name2))
