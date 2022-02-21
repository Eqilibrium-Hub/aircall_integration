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
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'queue_job'],
    # install python requests library for queue module

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/aircall_user_views.xml',
        'views/aircall_menus.xml'

    ],

    'application': True
}
