from odoo import models, fields, api
import datetime
import base64


class AccountMove(models.Model):
    _inherit = "account.move"

    is_factoring = fields.Boolean(
        compute='_compute_is_factoring', string='Is Factoring', store=True)
    generate_file = fields.Boolean(
        string="Data File", default=True, help="True = Generate data into faktura.sfg/kunde.sgf  \nFalse = Don't want generate data into faktura.sfg/kunde.sgf")

    @api.depends('partner_id')
    def _compute_commercial_partner_id(self):
        '''selecting commercial partner id in account_move model select
            if is factoring true then commercial tranzection go with company id that select in setting
            rather prosess with partner that id goes to partner ledger'''
        result = super()._compute_commercial_partner_id()
        for move in self.filtered(lambda move_id: move_id.is_factoring):
            move.commercial_partner_id = move.company_id.partner_id
        return result

    @api.depends('partner_id')
    def _compute_is_factoring(self):
        '''selecting is_factoring true when partner id is_factoring true rather
        selecting that perent is_factoring true'''
        for move in self:
            move.is_factoring = move.partner_id.is_factoring or move.partner_id.parent_id.is_factoring or False

    # @api.onchange('partner_id')
    # def _onchange_is_factoring(self):
    #     print("onchangre called")
    #     '''selecting is_factoring true when partner id is_factoring true rather
    #     selecting that perent is_factoring true'''
    #     for move in self:
    #         move.is_factoring = move.partner_id.is_factoring or move.partner_id.parent_id.is_factoring or False

    @api.depends('move_type', 'partner_id', 'company_id')
    def _compute_narration(self):
        '''is_factoring true then get narration thru assignment clause from settings
        rather selecting invoice_terms '''
        move = super()._compute_narration()
        for rec in self.filtered(lambda move_id: move_id.is_factoring):
            rec.narration = self.company_id.assignment_clause
        return move

    @api.depends('partner_id')
    def _compute_partner_bank_id(self):
        '''select partner bank id from there banks where in that user bank select default bank where
        is_factoring is true'''
        move = super()._compute_partner_bank_id()
        for user_bank in self.partner_id.bank_ids.filtered(lambda move_id: move_id.is_factoring):
            self.partner_bank_id = user_bank.id
        return move

    def luhn_checksum(self, invoice_number):
        ''' Luhn checksum for add last digit in payment_reference'''
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

    def _get_invoice_computed_reference(self):
        ''' generate value payment_reference'''
        pedding_value_undifined_lenth = str((self.name).split('/')[2])[:8]
        val = '91195'+pedding_value_undifined_lenth.zfill(8)+'00'
        return val + str(self.luhn_checksum(val))

    def run_cron_for_invoice_file(rec):
        ''' cron for create invoice file'''
        text = ""
        F1 = (str(1 if rec.move_type == 'out_invoice' else 9))
        F2 = ('1195')
        fieldF3 = rec.partner_id.parent_id.ref or rec.partner_id.ref or True
        F3 = (fieldF3[:9]).zfill(9) if type(fieldF3) != bool else "0"*9
        F4 = ((((rec.name).split("/")[2])[:8]).zfill(8)
              if (rec.name) else ''.zfill(8))
        F5 = ((rec.invoice_date).strftime(
            "%y%m%d") if type(rec.invoice_date) == datetime.date else "000000")
        F6 = ((rec.invoice_date_due).strftime(
            "%y%m%d") if type(rec.invoice_date_due) == datetime.date else "000000")
        F7 = (str(rec.amount_total_signed).zfill(11))
        final_discount_value = ''
        if (rec.invoice_date and rec.invoice_date_due) and rec.invoice_date <= rec.invoice_date_due:
            diff_days = (rec.invoice_date_due-rec.invoice_date).days
            final_discount_value = str(diff_days).zfill(
                3)+(str(rec.invoice_payment_term_id.line_ids.discount_percentage).replace(".", ""))
        F8 = (final_discount_value.zfill(5)[:5])
        F9 = (" "*8)
        F10 = (" "*15)
        F11 = (" "*25)
        F12 = (" "*4)
        F13 = (" "*7)
        F14 = (''.ljust(3))
        F15 = (" "*11)
        text += F1+F2+F3+F4+F5+F6+F7+F8+F9+F10+F11+F12+F13+F14+F15+'\r\n'
        return text

    def run_cron_for_debtor_file(rec):
        ''' cron for create debtor file'''
        text = ""
        k1 = ("k")
        k2 = ("9409")
        k3 = ("1195")
        fieldK4 = rec.partner_id.parent_id.ref or rec.partner_id.ref or True
        k4 = (fieldK4[:9]).ljust(9) if not fieldK4 else " "*9
        k5 = (str(rec.partner_id.l10n_no_bronnoysund_number).ljust(
            11)[:11] if rec.partner_id.l10n_no_bronnoysund_number else " "*11)
        k6 = (str(rec.partner_id.name)[:35].ljust(
            35) if rec.partner_id.name else " "*35)
        k7 = ("".ljust(20))
        k8 = (str(rec.partner_id.street)[:30].ljust(
            30) if rec.partner_id.street else " "*30)
        k9 = ((str(rec.partner_id.zip)[:4].ljust(4))[
              :4] if rec.partner_id.zip else " "*4)
        k10 = (str(rec.partner_id.city)[:23].ljust(
            23) if rec.partner_id.city else " "*23)
        k11 = (" "*20)
        k12 = (" "*12)
        k13 = ("Norge".ljust(20))
        k14 = ("NO")
        k15 = ("578")
        k16 = (" "*11)
        k17 = (" "*4)
        k18 = (" "*35)
        k19 = ("NOK")
        text += k1+k2+k3+k4+k5+k6+k7+k8+k9+k10+k11 + \
            k12+k13+k14+k15+k16+k17+k18+k19+'\r\n'
        return (text)

    def run_cron_job(self):
        '''cron job for calling invoice and debtor cron job funaction and calling templete'''
        invoice_text = ''
        debtor_text = ''
        for move in self.search([('state', '=', 'posted'), ('generate_file', '=', True), ('is_factoring', '=', True)]):
            if move.move_type in ('out_refund', 'out_invoice'):
                invoice_text += move.run_cron_for_invoice_file()
                debtor_text += move.run_cron_for_debtor_file()

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
            'name': f'kunde_{time}.sgf',
            'folder_id': folder_id,
        })
