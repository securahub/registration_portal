from odoo import models, fields

class RegistrationSubmission(models.Model):
    _name = 'registration.submission'
    _description = 'Registration Submission'

    link_id = fields.Many2one('registration.link', string='Registration Link', required=True)
    name = fields.Char(string='Applicant Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    address = fields.Text(string='Address')
    course = fields.Selection([
        ('ciap', 'CIAP'),
        ('cma_usa', 'CMA USA'),
        ('ca', 'CA'),
        ('cma_india', 'CMA INDIA'),
        ('acca', 'ACCA'),
    ], string='Course')

    district = fields.Selection([
        ('thiruvananthapuram', 'Thiruvananthapuram'),
        ('kollam', 'Kollam'),
        ('pathanamthitta', 'Pathanamthitta'),
        ('alappuzha', 'Alappuzha'),
        ('kottayam', 'Kottayam'),
        ('idukki', 'Idukki'),
        ('ernakulam', 'Ernakulam'),
        ('thrissur', 'Thrissur'),
        ('palakkad', 'Palakkad'),
        ('malappuram', 'Malappuram'),
        ('kozhikode', 'Kozhikode'),
        ('wayanad', 'Wayanad'),
        ('kannur', 'Kannur'),
        ('kasaragod', 'Kasaragod'),
    ], string='District')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)
    state = fields.Selection([
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('done', 'Done')
    ], string='Status', default='new')
    
    value_ids = fields.One2many('registration.submission.value', 'submission_id', string='Custom Values')

    def action_create_lead(self):
        for rec in self:
            if not rec.phone:
                from odoo.exceptions import ValidationError
                raise ValidationError("Phone number is required to create a lead.")
            
            source = self.env['leads.sources'].search([('name', '=', 'Registration Portal')], limit=1)
            if not source:
                source = self.env['leads.sources'].create({'name': 'Registration Portal'})
                
            course_name = dict(self._fields['course'].selection).get(rec.course) if rec.course else ''
            
            lead_vals = {
                'name': rec.name,
                'email_address': rec.email,
                'phone_number': rec.phone,
                'leads_source': source.id,
                'district': rec.district,
                'place': rec.address,
                'course_interested': course_name,
            }
            lead = self.env['leads.logic'].sudo().create(lead_vals)
            rec.state = 'done'
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Lead',
                'res_model': 'leads.logic',
                'res_id': lead.id,
                'view_mode': 'form',
                'target': 'current',
            }
