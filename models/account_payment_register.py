from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def _compute_partner_bank_id(self):
        # Method set value partner_bank_id field
        # data set from account.move model method is  action_register_payment
        res = super(AccountPaymentRegister, self)._compute_partner_bank_id()
        for wizard in self:
            wizard.partner_bank_id = self.env['res.partner.bank'].search(
                [('id', '=', self._context.get('partner_payment_id'))])
        return res
