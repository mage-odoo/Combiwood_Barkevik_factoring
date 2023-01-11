from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta


class AccountMove(models.Model):
    _inherit = "account.move"
    is_factoring = fields.Boolean(
        string='Is Factoring', readonly=True)
    is_file_generated = fields.Boolean(
        string="Data File", help="True = Generate data into faktura.sfg", default=True)

    @api.depends('partner_id')
    def _compute_commercial_partner_id(self):
        partner_account_id = 0
        for rec in self.env['assignment.clause.value'].search([]):
            assignemt_value = rec.assignment_clause
            partner_account_id = rec.partner_account_id
        for move in self:
            move.commercial_partner_id = partner_account_id

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        # if you change manually invoice partner id field
        # then partner_bank_id value change if is_factoring True
        res = super(AccountMove, self)._onchange_partner_id()
        for user_bank in self.partner_id.bank_ids:
            if user_bank.is_factoring == True:
                self.partner_bank_id = user_bank.id
                break
        return res

    def _get_invoice_computed_reference(self):
        print("compute called")
        pedding_value_undifined_lenth = str((self.name).split('/')[2])
        val = '91195'+pedding_value_undifined_lenth.zfill(8)+'00'
        return val + str(AccountMove.luhn_checksum(val))

    def luhn_checksum(invoice_number):
        # Luhn checksum for add last digit in payment_reference
        def digits_of(n):
            return [int(d) for d in str(n)]
        digits = digits_of(invoice_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d*2))
        return str(checksum % 10)

    def run_cron_job(self):
        AccountMove.run_cron_for_invoice_file(self)
        AccountMove.run_cron_for_debtor_file(self)

    def run_cron_for_invoice_file(self):
        open("faktura.sgf", "w").close()
        f = open("faktura.sgf", "a", encoding="utf-16")
        for rec in self.env['account.move'].search([('is_file_generated', '=', 'True'), ('move_type', '!=', 'entry')]):
            f.write(str(1 if rec.move_type == 'out_invoice' else 9))
            f.write('1195')
            f.write(str(rec.partner_id.id).zfill(9))
            f.write(((rec.name).split("/")[2]).zfill(8))
            f.write((rec.invoice_date).strftime("%y%m%d"))
            f.write((rec.invoice_date_due).strftime("%y%m%d"))
            f.write(str(abs(rec.amount_total_signed)).zfill(11))
            print(rec.invoice_payment_term_id.line_ids.discount_days)
            last_discount_date = (rec.create_date).date() + \
                timedelta(days=10)
            finalvalue = ''
            if (rec.invoice_date) <= last_discount_date:
                finalvalue = "0"+str(rec.invoice_payment_term_id.line_ids.discount_days) + \
                                    (str(rec.invoice_payment_term_id.line_ids.discount_percentage).replace(
                                        ".", ""))
                print(rec.invoice_payment_term_id.line_ids.discount_days)
            f.write(finalvalue.zfill(5))
            f.write(" "*8)
            f.write(" "*15)
            f.write(" "*25)
            f.write(" "*4)
            f.write(" "*7)
            f.write((rec.name)[:3])
            f.write(" "*11)
            f.write("\n")
        f.close()
        with open("faktura.sgf", "r", encoding="utf-16") as myfile:
            print(myfile.read())

    def run_cron_for_debtor_file(self):
        open("kunde.sgf", "w").close()
        f = open("kunde.sgf", "a", encoding="utf-16")
        for rec in self.env['res.partner'].search([]):
            f.write("k")
            f.write("9409")
            f.write("1195")
            f.write(str(rec.ref).ljust(9))
            f.write(str(rec.l10n_no_bronnoysund_number).ljust(11)[:11])
            f.write(str(rec.name).ljust(35))
            f.write(str("N/A").ljust(20))
            f.write(str(rec.street).ljust(30))
            f.write((str(rec.zip).ljust(4))[:4])
            f.write(str(rec.city).ljust(23))
            f.write(" "*20)
            f.write(" "*12)
            f.write("Norge".ljust(20))
            f.write("NO")
            f.write("578")
            f.write(" "*11)
            f.write(" "*4)
            f.write(" "*35)
            f.write("NOK")
            f.write("\n")
        f.close()
        with open("kunde.sgf", "r", encoding="utf-16") as myfile:
            print(myfile.read())
