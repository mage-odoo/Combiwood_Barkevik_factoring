from odoo import models, fields, api


class assignment_clause_value(models.Model):
    _name = 'assignment.clause.value'
    assignment_clause = fields.Text(
        string="Assignment Clause", default="test data")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    is_factoring = fields.Boolean(string='Is Factoring', default=True)
    assignemt_clause_id = fields.Many2one(
        'assignment.clause.value', string='Assignemt Clause')
    # default="Fordringer etter nærværende faktura er overdratt DNB Bank ASA, Postboks 1600 Sentrum, 0021 Oslo, til eiendom. Befriende betaling kan kun skje til DNB Bank ASA. Bankkonto 7032.05.16038. Ved betaling vennligst oppgi KID- referanse eller fakturanummer og leverandør.")
    assignment_clause = fields.Text(
        string="Assignment Clause", store=True, readonly=False)  # , related='assignemt_clause_id.assignment_clause')

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        assignemt_value = ''
        print("get called")
        for rec in self.env['assignment.clause.value'].search([]):
            assignemt_value = rec.assignment_clause
        res.update(
            assignment_clause=assignemt_value)
        return res

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        for rec in self:
            if rec.assignment_clause:
                self.env['assignment.clause.value'].search([]).unlink()
                print(rec.assignment_clause)
                self.env['assignment.clause.value'].create({'id': '1',
                                                           'assignment_clause': rec.assignment_clause})
        return res