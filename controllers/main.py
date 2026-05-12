from odoo import http
from odoo.http import request

class RegistrationController(http.Controller):

    @http.route('/registration/<string:slug>', type='http', auth='public', website=True)
    def registration_form(self, slug, **kwargs):
        link_id = request.env['registration.link'].sudo().search([('slug', '=', slug), ('active', '=', True)], limit=1)
        if not link_id:
            return request.not_found()
        
        return request.render('registration_portal.registration_form_template', {
            'link': link_id,
        })

    @http.route('/registration/submit', type='http', auth='public', website=True, methods=['POST'], csrf=False)
    def registration_submit(self, **post):
        link_slug = post.get('link_slug')
        link_id = request.env['registration.link'].sudo().search([('slug', '=', link_slug), ('active', '=', True)], limit=1)
        
        if not link_id:
            return request.not_found()

        vals = {
            'link_id': link_id.id,
            'name': post.get('name'),
            'email': post.get('email'),
            'phone': post.get('phone'),
            'course': post.get('course'),
            'district': post.get('district'),
        }
        
        submission = request.env['registration.submission'].sudo().create(vals)

        # Process Custom Fields
        for field in link_id.field_ids:
            input_name = 'custom_field_%s' % field.id
            value = post.get(input_name)
            if value:
                request.env['registration.submission.value'].sudo().create({
                    'submission_id': submission.id,
                    'field_id': field.id,
                    'value': value,
                })

        # Send Zoom Link Email if configured
        if link_id.zoom_link and submission.email:
            template = request.env.ref('registration_portal.registration_email_template', raise_if_not_found=False)
            if template:
                template.sudo().send_mail(submission.id, force_send=True)
        
        return request.render('registration_portal.registration_success_template', {
            'link': link_id,
        })
