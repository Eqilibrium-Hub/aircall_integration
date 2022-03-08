# -*- coding: utf-8 -*-
{
    'name': "aircall_integration",

    'summary': """
        Aircall integration into Odoo.""",

    'description': """
        todo
    """,

    'author': "Lagneau Gaétan",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    'depends': [
        'base',
        'web',
        'omar_audio'  # audio widget
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/aircall_menus.xml',
        'views/res_config_settings_views.xml',
        'views/aircall_call_view.xml',
        'data/call_expiry_cron.xml'

    ],
    'application': True,
    'license': 'LGPL-3'
}
