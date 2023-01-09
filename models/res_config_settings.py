from odoo import models, fields, api


class assignment_clause_value(models.Model):
    # Model for save just assignemt_clause_id single(one) value
    _name = 'assignment.clause.value'
    _description = "Model for save just assignemt_clause_id single(one) value"
    assignment_clause = fields.Html(
        string="Assignment Clause", default="test data")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    is_factoring = fields.Boolean(string='Is Factoring', default=True)
    assignemt_clause_id = fields.Many2one(
        'assignment.clause.value', string='Assignemt Clause')
    assignment_clause = fields.Html(
        string="Assignment Clause", store=True, readonly=False)

    @api.model
    # THIS METHOD USE FOR INSERT DATA res.config.settings WHILE DATA LOAD AT FIRST TIME
    # SOME OF DATA FETCH ANOTHER MODEL assignment.clause.value AND UPDATE IT
    # PREDIFINE FUNCTION OVERRIDE
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        assignemt_value = ''
        for rec in self.env['assignment.clause.value'].search([]):
            assignemt_value = rec.assignment_clause
        res.update(
            assignment_clause=assignemt_value
        )
        return res

    def set_values(self):
        # THIS METHOD USE FOR SET DATA WHEN YOU CLICK SAVE BUTTON AT res.config.settings
        # DATA ARE SAVE AT assignment.clause.value MODEL
        res = super(ResConfigSettings, self).set_values()
        for rec in self:
            if rec.assignment_clause:
                for val_of_assignment_clause in self.env['assignment.clause.value'].search([]):
                    print("onsert value for")
                    if hash(rec.assignment_clause) != hash(val_of_assignment_clause.assignment_clause):
                        print("onsert value if")
                        self.env['assignment.clause.value'].search([]).unlink()
                        print(rec.assignment_clause)
                        self.env['assignment.clause.value'].create({'id': '1',
                                                                    'assignment_clause': rec.assignment_clause})
                else:
                    self.env['assignment.clause.value'].create({'id': '1',
                                                                'assignment_clause': rec.assignment_clause})
        for i in self.env['assignment.clause.value'].search([]):
            print(i.assignment_clause)
        return res
