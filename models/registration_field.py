from odoo import models, fields, api

class RegistrationField(models.Model):
    _name = 'registration.field'
    _description = 'Registration Form Field'
    _order = 'sequence'

    link_id = fields.Many2one('registration.link', string='Registration Link', required=True, ondelete='cascade')
    name = fields.Char(string='Label', required=True)
    key = fields.Char(string='Technical Key', help='Unique key for the field (e.g. age, father_name)')
    field_type = fields.Selection([
        ('char', 'Single Line Text'),
        ('text', 'Multi Line Text'),
        ('integer', 'Number'),
        ('date', 'Date'),
        ('selection', 'Selection'),
        ('binary', 'File Upload'),
    ], string='Field Type', required=True, default='char')
    required = fields.Boolean(string='Required', default=False)
    sequence = fields.Integer(string='Sequence', default=10)
    selection_options = fields.Text(string='Selection Options', help='Comma separated options for Selection type (e.g. Male,Female,Other)')

    @api.model
    def create(self, vals):
        if not vals.get('key'):
             # Simple slugify for key if not provided
             vals['key'] = (vals.get('name') or '').lower().replace(' ', '_')
        return super(RegistrationField, self).create(vals)
