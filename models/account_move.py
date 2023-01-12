from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta
import base64


class AccountMove(models.Model):
    _inherit = "account.move"
    is_factoring = fields.Boolean(
        string='Is Factoring', readonly=True)
    is_file_generated = fields.Boolean(
        string="Data File", help="True = Generate data into faktura.sfg  \nFalse = don'twant Generate data into faktura.sfg")

    def _compute_commercial_partner_id(self):
        # res = sum(AccountMove, self)._compute_commercial_partner_id()
        for move in self:
            if move.company_id.partner_id:
                move.commercial_partner_id = move.company_id.partner_id
        # return res

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
        invoice_text = ''
        debtor_text = ''
        for rec in self.env['account.move'].search([('move_type', '!=', 'entry'), ('state', '!=', 'draft'), ('is_file_generated', '=', 'False')]):
            invoice_text += AccountMove.run_cron_for_invoice_file(rec)
        for rec in self.env['res.partner'].search([]):
            debtor_text += AccountMove.run_cron_for_debtor_file(rec)
        # File Generate code
        folder_id = self.env.ref(
            'Combiwood_Barkevik_factoring.documents_internal_folder').id
        row = {'row': invoice_text}
        time = str(fields.date.today())
        datas, dummy = self.env["ir.actions.report"]._render_qweb_text(
            'Combiwood_Barkevik_factoring.action_report_invoice_file', self, row)
        document_gif = self.env['documents.document'].create({
            'datas': base64.b64encode(datas),
            'name':  time+'_faktura.sgf',
            'folder_id': folder_id,
        })
        row = {'row': debtor_text}
        datas, dumxxmy = self.env["ir.actions.report"]._render_qweb_text(
            'Combiwood_Barkevik_factoring.action_report_deptor_file', self, row)
        document_gif = self.env['documents.document'].create({
            'datas': base64.b64encode(datas),
            'name': time+'_kunde.sgf',
            'folder_id': folder_id,
        })

    def run_cron_for_invoice_file(rec):
        text = ""
        F1 = (str(1 if rec.move_type == 'out_invoice' else 9))
        F2 = ('1195')
        F3 = (str(rec.partner_id.id).zfill(9))
        F4 = ((((rec.name).split("/")[2])[:8]).zfill(8)
              if (rec.name) else ''.zfill(8))
        F5 = ((rec.invoice_date).strftime(
            "%y%m%d") if rec.invoice_date else "000000")
        F6 = ((rec.invoice_date_due).strftime(
            "%y%m%d") if rec.invoice_date else "000000")
        F7 = (str(abs(rec.amount_total_signed)).zfill(11))
        finalvalue = ''
        if rec.invoice_date:
            last_discount_date = (rec.create_date).date() + \
                timedelta(days=10)
            if (rec.invoice_date) <= last_discount_date:
                finalvalue = "0"+str(rec.invoice_payment_term_id.line_ids.discount_days) + \
                                    (str(rec.invoice_payment_term_id.line_ids.discount_percentage).replace(
                                        ".", ""))
        F8 = (finalvalue.zfill(5))
        F9 = (" "*8)
        F10 = (" "*15)
        F11 = (" "*25)
        F12 = (" "*4)
        F13 = (" "*7)
        F14 = ((rec.name)[:3] if (rec.name) else ''.zfill(3))
        F15 = (" "*11)
        text += F1+F2+F3+F4+F5+F6+F7+F8+F9+F10+F11+F12+F13+F14+F15+"\n"
        return text

    def run_cron_for_debtor_file(rec):
        text = ""
        k1 = ("k")
        k2 = ("9409")
        k3 = ("1195")
        k4 = (str(rec.ref).ljust(9) if rec.ref else " "*9)
        k5 = (str(rec.l10n_no_bronnoysund_number).ljust(
            11)[:11] if rec.ref else " "*11)
        k6 = (str(rec.name).ljust(35) if rec.ref else " "*35)
        k7 = (str("N/A").ljust(20))
        k8 = (str(rec.street).ljust(30) if rec.ref else " "*30)
        k9 = ((str(rec.zip).ljust(4))[:4] if rec.ref else " "*4)
        k10 = (str(rec.city).ljust(23) if rec.ref else " "*23)
        k11 = (" "*20)
        k12 = (" "*12)
        k13 = ("Norge".ljust(20))
        k14 = ("NO")
        k15 = ("578")
        k16 = (" "*11)
        k17 = (" "*4)
        k18 = (" "*35)
        k19 = ("NOK")
        text += k1+k2+k3+k4+k5+k6+k7+k8+k9+k10+k11+k12+k13+k14+k15+k16+k17+k18+k19+"\n"
        return (text)
