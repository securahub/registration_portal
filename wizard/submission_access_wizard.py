from odoo import models, fields, exceptions, _

class RegistrationSubmissionAccessWizard(models.TransientModel):
    _name = 'registration.submission.access.wizard'
    _description = 'Submission Access Wizard'

    link_id = fields.Many2one('registration.link', string='Link', required=True)
    password = fields.Char(string='Password', required=True)

    def action_confirm(self):
        self.ensure_one()
        if self.link_id.access_password and self.password != self.link_id.access_password:
             raise exceptions.AccessDenied(_("Incorrect Password"))
        
        return {
            'name': _('Submissions'),
            'type': 'ir.actions.act_window',
            'res_model': 'registration.submission',
            'view_mode': 'tree,form',
            'domain': [('link_id', '=', self.link_id.id)],
            'context': {'default_link_id': self.link_id.id},
        }
