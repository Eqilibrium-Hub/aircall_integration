# -*- coding: utf-8 -*-
{
    'name': "aircall_integration",

    'summary': """
        Aircall integration into Odoo.""",

    'description': """
        Aircall
        ==================================
        This module is a custom connector between Odoo and Aircall.
        It uses the aircall API, as well as its webhooks, to exchange information.
        Aircall webhooks require the endpoint to be https secured, so make
        sure you odoo instance has that. 

        Main Features
        -------------
        * Log your calls
            - includes recording, tags, direction, duration ...
            - retrieves the caller and the callee as Odoo users
            - cron to clean logs periodically 
        * (To come) Insights Cards (https://aircall.io/fr/fonctionnalites-standard-telephonique-virtuel/insight-cards/)
            - link to the odoo profile of the callee is displayed to the agent
            - information on the callee (leads, account owner ?)
        * (To come) Contacts Synchronization
            - every odoo contact is registered on aircall and vice versa   
    """,

    'author': "Lagneau Gaétan",
    'category': 'Administration',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'omar_audio'  # audio widget
    ],

    'external_dependencies': {
        'python': [
            'phonenumbers'
        ],
    },

    'data': [
        'security/ir.model.access.csv',
        'views/aircall_menus.xml',
        'views/res_config_settings_views.xml',
        'views/aircall_call_view.xml',
        'views/res_users_views.xml',
        'data/call_expiry_cron.xml'
    ],
    'application': True,
    'license': 'LGPL-3'
}
