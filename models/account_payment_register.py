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

    # def default_get(self, fields_list):
    #     res = super(AccountPaymentRegister, self).default_get(fields_list)
    #     # print(self._context.get('partner_payment_id'))
    #     res['partner_payment_id'] = self._context.get('partner_payment_id')
    #     print(res['partner_payment_id'])
    #     # if self._context.get('active_model') == 'account.move':
    #     #     lines = self.env['account.move'].browse(
    #     #         self._context.get('partner_payment_id'))
    #     #     print(lines)
    #     return res
