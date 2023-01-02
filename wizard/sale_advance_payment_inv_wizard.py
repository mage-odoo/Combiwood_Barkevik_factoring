from odoo import models, fields, api


class temp:
    t1 = 2


class advance_payment_inv_inherit(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'
    is_factoring_temp = fields.Boolean(
        string='Is Factoring', related='sale_order_ids.is_factoring')

    def create_invoices(self):
        temp.t1 = self.is_factoring_temp
        print("onchange called", self.sale_order_ids.is_factoring)
        # self.is_factoring = self.sale_order_ids.is_factoring
        # print("done calling.............................", temp.t1)
        super(advance_payment_inv_inherit, self).create_invoices()
