{
    'name': 'Registration Portal',
    'version': '1.0',
    'category': 'Website',
    'summary': 'Dynamic Registration Portal',
    'description': """
        This module allows users to create dynamic registration links and collect data via a public portal.
    """,
    'author': 'Antigravity',
    'depends': ['base', 'web', 'website', 'portal', 'mail'],
    'data': [
        'security/registration_security.xml',
        'security/ir.model.access.csv',
        'data/mail_template_data.xml',
        'views/registration_link_views.xml',
        'views/registration_submission_views.xml',
        'wizard/submission_access_wizard_views.xml',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': True,
}
