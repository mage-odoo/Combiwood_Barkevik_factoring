from odoo import models, fields, api


class assignment_clause_value(models.Model):
    # Model for save just assignemt_clause_id single(one) value
    _name = 'assignment.clause.value'
    _description = "Model for save just assignemt_clause_id single(one) value"
    assignment_clause = fields.Html(
        string="Assignment Clause", default="test data")
    partner_account_id = fields.Integer()


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    is_factoring = fields.Boolean(string='Is Factoring', default=lambda self:self.env.user.is_factoring)
    res_company_id = fields.Many2one(
        'res.company', default=lambda self:self.env.user.company_id.id)
    assignment_clause = fields.Html(
        string="Assignment Clause",related='res_company_id.assignment_clause',store=True,readonly=False)
    partner_account_id = fields.Many2one(
        'res.partner', string='partner_account_id',related='res_company_id.partner_account_id',store=True,readonly=False)
    
