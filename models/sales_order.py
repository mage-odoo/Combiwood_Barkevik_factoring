from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = "sale.order"
    is_factoring = fields.Boolean(
        compute='_compute_is_factoring', tracking=True, readonly=False, store=True, string='is_factoring')

    @api.depends('partner_invoice_id')
    def _compute_is_factoring(self):
        for rec in self:
            rec.is_factoring = rec.partner_invoice_id.is_factoring or rec.partner_invoice_id.parent_id.is_factoring or False

    # def _prepare_invoice(self):
    #     # click 'Create Invoice' button set defult invoice_val value
    #     # for account.move model
    #     invoice_val = super(SalesOrder, self)._prepare_invoice()
    #     invoice_val["is_factoring"] = self.is_factoring
    #     # invoice_partner_display_name
    #     is_factoring_display_text = self.company_id.assignment_clause
    #     partner_account_id = self.company_id.partner_id
    #     if self.is_factoring == True:
    #         invoice_val["narration"] = is_factoring_display_text
    #         invoice_val['invoice_partner_display_name'] = partner_account_id
    #     for rec in self.env['res.partner.bank'].search(
    #             [('partner_id.id', '=', invoice_val["partner_id"])]):
    #         if rec.is_factoring == True:
    #             invoice_val['partner_bank_id'] = rec.id
    #     return invoice_val
