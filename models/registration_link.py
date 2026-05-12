from odoo import models, fields, api
import uuid

class RegistrationLink(models.Model):
    _name = 'registration.link'
    _description = 'Registration Link'

    name = fields.Char(string='Event Name', required=True)
    slug = fields.Char(string='Link Slug', required=True, copy=False, unique=True)
    description = fields.Html(string='Description')
    program_details = fields.Html(string='Program Details (Success Page)')
    program_image = fields.Binary(string='Program Image')
    zoom_link = fields.Char(string='Zoom Link')
    active = fields.Boolean(default=True)
    submission_ids = fields.One2many('registration.submission', 'link_id', string='Submissions')
    field_ids = fields.One2many('registration.field', 'link_id', string='Custom Fields')
    access_password = fields.Char(string='Access Password', help='Password required to view submissions in the backend')
    is_super_admin = fields.Boolean(compute='_compute_is_super_admin', string='Is Super Admin')

    def _compute_is_super_admin(self):
        for record in self:
            record.is_super_admin = self.env.user.has_group('base.group_system')

    def action_view_submissions(self):
        self.ensure_one()
        # If user is system admin, bypass password
        if self.env.user.has_group('base.group_system') or not self.access_password:
             return {
                'name': 'Submissions',
                'type': 'ir.actions.act_window',
                'res_model': 'registration.submission',
                'view_mode': 'tree,form',
                'domain': [('link_id', '=', self.id)],
                'context': {'default_link_id': self.id},
            }
        # Otherwise open wizard
        return {
            'name': 'Enter Password',
            'type': 'ir.actions.act_window',
            'res_model': 'registration.submission.access.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_link_id': self.id},
        }

    @api.model
    def create(self, vals):
        if not vals.get('slug'):
             vals['slug'] = str(uuid.uuid4())
        return super(RegistrationLink, self).create(vals)
