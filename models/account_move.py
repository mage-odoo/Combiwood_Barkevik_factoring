from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"
    is_factoring = fields.Boolean(
        string='Is Factoring', readonly=True)

    def action_register_payment(self):
        # set context in partner_payment_id for fetch account_payment_register
        # and set partner_payment_id
        res = super(AccountMove, self).action_register_payment()
        res['context']['partner_payment_id'] = self.partner_bank_id.id
        return res

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

    def _post(self, soft=True):
        # Method - adding payment_reference value accoding to sequence in account.account_move
        # define prefix and suffix and  luhn_checksum for accidental errors adding end of value

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
        res = super(AccountMove, self)._post(soft)
        if type(self.payment_reference) == str and self.payment_reference not in 'INV/':
            print("post called", self.payment_reference)
            payment_reference_seq = self.env['ir.sequence'].search([
                ('code', '=', 'account.account_move')
            ])
            pedding_value_undifined_lenth = (
                self.payment_reference).split('/')[2]
            pedding_value_differnce = payment_reference_seq.padding - \
                len(pedding_value_undifined_lenth)
            if pedding_value_differnce < 0:
                raise ValidationError(
                    _("In Sequence -> account.account_move -> Sequence Size is less then invoice id\nIncrement Sequence Size {0} or more then {0}".format(len(pedding_value_undifined_lenth))))
            pedding_value = ('0'*pedding_value_differnce) + \
                str(pedding_value_undifined_lenth)
            after_payment_reference_value = payment_reference_seq.prefix + \
                pedding_value+payment_reference_seq.suffix
            self.payment_reference = after_payment_reference_value + \
                luhn_checksum(after_payment_reference_value)

        return res

    def button_draft(self):
        # This function remove payment_reference field data
        res = super(AccountMove, self).button_draft()
        for move in self:
            move.payment_reference = ''
        return res

    @api.onchange('partner_bank_id')
    def _onchange_partner_id(self):
        print(self.partner_bank_id)
