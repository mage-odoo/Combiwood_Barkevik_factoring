from odoo import models, fields, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    def default_get(self):
        res = super(AccountPaymentRegister, self).default_get()
        print("default get called")
        return res
