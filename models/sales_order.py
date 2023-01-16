from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = "sale.order"

    is_factoring = fields.Boolean(
        compute='_compute_is_factoring', readonly=False, store=True, string='Is Factoring')

    @api.depends('partner_invoice_id')
    def _compute_is_factoring(self):
        '''if is_facroring  true when invoice address is differant from partner_id
        rather go for that perent '''
        for rec in self:
            rec.is_factoring = rec.partner_invoice_id.is_factoring or rec.partner_invoice_id.parent_id.is_factoring or False

    # def _prepare_invoice(self):
    #     # click 'Create Invoice' button set defult invoice_val value
    #     # for account.move model
    #     invoice_val = super(SalesOrder, self)._prepare_invoice()
    #     invoice_val["is_factoring"] = self.is_factoring
    #     return invoice_val
