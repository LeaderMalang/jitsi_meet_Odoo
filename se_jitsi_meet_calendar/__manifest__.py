# -*- coding: utf-8 -*-
# © 2020     Sinerkia iD (<https://www.sinerkia.com>).
{
    'name': 'Video Call/Conference with Jitsi Meet. Integration with Odoo Calendar',
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
'website': "https://softwareescarlata.com/",
    'sequence': 1,
    'summary': 'Create and share Jitsi Meet video conferences with other users',
    'description': """
		Adds a new APP to create and share Jisti Meet video conference meetings between Odoo users.
		When you join the meeting Odoo opens a new browser tab so you can keep working on Odoo, and share screen with your partners at Jisti Meet. 
		
		website
		elearning
		call
		video
		
    """,
    'author': "David Montero Crespo",
    "depends": ['base','web','mail','calendar','website'],
    "data": [
        'views/se_jitsi_meet_views.xml',
        'views/template.xml',
        'data/se_jitsi_meet.xml',
        'data/mail_template.xml',
    ],
    'images': ['static/description/0.jpg'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 40,
    'currency': 'EUR',
    'license': 'AGPL-3',
}
