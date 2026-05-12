from odoo import models, fields

class RegistrationSubmissionValue(models.Model):
    _name = 'registration.submission.value'
    _description = 'Registration Submission Value'

    submission_id = fields.Many2one('registration.submission', string='Submission', required=True, ondelete='cascade')
    field_id = fields.Many2one('registration.field', string='Field', required=True, ondelete='cascade')
    value = fields.Text(string='Value')
