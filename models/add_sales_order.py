from odoo import models, fields, api


class AddSalesOrder(models.Model):
    _inherit = "sale.order"
    is_factoring = fields.Boolean(string='Is Factoring', tracking=True)

    @api.onchange('partner_id')
    def _onchange_is_factoring(self):
        self.is_factoring = self.partner_id.is_factoring

    def _prepare_invoice(self):
        invoice_val = super(AddSalesOrder, self)._prepare_invoice()
        invoice_val["is_factoring"] = self.is_factoring
        is_factoring_display_text = ''
        if self.is_factoring == True:
            for rec in self.env['assignment.clause.value'].search([]):
                is_factoring_display_text = rec.assignment_clause
            invoice_val["narration"] = is_factoring_display_text
        # print(invoice_val["partner_id"])
        print(self.env['res.partner.bank'].search(['partner_id','=',str(invoice_val["partner_id"]) ]))

        return invoice_val
