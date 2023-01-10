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
    is_factoring = fields.Boolean(string='Is Factoring', default=True)
    assignemt_clause_id = fields.Many2one(
        'assignment.clause.value', string='Assignemt Clause')
    assignment_clause = fields.Html(
        string="Assignment Clause", store=True, readonly=False)
    partner_account_id = fields.Many2one(
        'res.partner', string='partner_account_id')

    @ api.model
    # THIS METHOD USE FOR INSERT DATA res.config.settings WHILE DATA LOAD AT FIRST TIME
    # SOME OF DATA FETCH ANOTHER MODEL assignment.clause.value AND UPDATE IT
    # PREDIFINE FUNCTION OVERRIDE
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        assignemt_value = ''
        partner_account_id = 0
        for rec in self.env['assignment.clause.value'].search([]):
            assignemt_value = rec.assignment_clause
            partner_account_id = rec.partner_account_id
        res.update(
            assignment_clause=assignemt_value,
            partner_account_id=partner_account_id
        )
        return res

    def set_values(self):
        # THIS METHOD USE FOR SET DATA WHEN YOU CLICK SAVE BUTTON AT res.config.settings
        # DATA ARE SAVE AT assignment.clause.value MODEL
        res = super(ResConfigSettings, self).set_values()
        for rec in self:
            if rec.assignment_clause:
                for val_of_ in self.env['assignment.clause.value'].search([]):
                    if hash(rec.assignment_clause) != hash(val_of_.assignment_clause) and rec.partner_account_id.id != val_of_.partner_account_id:
                        assignment_clause = rec.assignment_clause
                        partner_account_id = rec.partner_account_id.id
                        self.env['assignment.clause.value'].search([]).unlink()
                        self.env['assignment.clause.value'].create({'partner_account_id': partner_account_id,
                                                                    'assignment_clause': assignment_clause})
                        break
                    elif hash(rec.assignment_clause) != hash(val_of_.assignment_clause):
                        assignment_clause = rec.assignment_clause
                        partner_account_id = rec.partner_account_id.id
                        self.env['assignment.clause.value'].search([]).unlink()
                        self.env['assignment.clause.value'].create({'partner_account_id': partner_account_id,
                                                                    'assignment_clause': assignment_clause})
                        break
                    elif rec.partner_account_id.id != val_of_.partner_account_id:
                        partner_account_id = rec.partner_account_id.id
                        assignment_clause = rec.assignment_clause
                        print("set value", partner_account_id)
                        self.env['assignment.clause.value'].search([]).unlink()
                        self.env['assignment.clause.value'].create({'assignment_clause': assignment_clause,
                                                                    'partner_account_id': partner_account_id})
                        break
                else:
                    self.env['assignment.clause.value'].search([]).unlink()
                    self.env['assignment.clause.value'].create({'partner_account_id': rec.partner_account_id.id,
                                                                'assignment_clause': rec.assignment_clause})
            # for rec_assignmet in self.env['assignment.clause.value'].search([]):
            #     self.env['assignment.clause.value'].search([]).unlink()
        return res
