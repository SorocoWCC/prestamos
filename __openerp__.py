# -*- coding: utf-8 -*-
{
    'name': "Manejo de  Prestamos",

    'summary': """
        Manejo de Prestamos""",

    'description': """
        Manejo de Prestamos
    """,

    'author': "Warren Castro",
    'website': "http://www.recicladorasanmiguel.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'prestamo_workflow.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
