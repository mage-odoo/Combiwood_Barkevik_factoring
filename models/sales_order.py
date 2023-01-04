from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = "sale.order"
    is_factoring = fields.Boolean(string='Is Factoring', tracking=True)

    @api.onchange('partner_id')
    def _onchange_is_factoring(self):
        # Method - set value same as preset in res.partner
        self.is_factoring = self.partner_id.is_factoring

    def _prepare_invoice(self):
        # click 'Create Invoice' button set defult invoice_val value
        # for account.move model
        invoice_val = super(SalesOrder, self)._prepare_invoice()
        invoice_val["is_factoring"] = self.is_factoring
        is_factoring_display_text = ''
        if self.is_factoring == True:
            for rec in self.env['assignment.clause.value'].search([]):
                is_factoring_display_text = rec.assignment_clause
            invoice_val["narration"] = is_factoring_display_text
        for rec in self.env['res.partner.bank'].search([]):
            print(rec.partner_id.id)
        for rec in self.env['res.partner.bank'].search(
                [('partner_id.id', '=', invoice_val["partner_id"])]):
            if rec.is_factoring == True:
                invoice_val['partner_bank_id'] = rec.bank_id.id
        return invoice_val
