from odoo import models, fields, api


class SalesOrder(models.Model):
    _inherit = "sale.order"
    is_factoring = fields.Boolean(string='Is Factoring', tracking=True)

    @api.onchange('partner_id')
    def _onchange_is_factoring(self):
        # Method - set value same as preset in res.partner
        self.is_factoring = self.partner_id.is_factoring

    @api.onchange('is_factoring')
    def _onchange_is_factoring(self):
        if self.is_factoring:
            for rec in self.env['assignment.clause.value'].search([]):
                self.note = rec.assignment_clause
        else:
            # order = order.with_company(order.company_id)
            self.note = self.with_context(
                lang=self.partner_id.lang).env.company.invoice_terms

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
            print(rec.acc_number)
            # if rec.is_factoring == True:
            #     invoice_val['partner_bank_id'] = rec.id
        print(invoice_val)
        return invoice_val
