# -*- coding: utf-8 -*-
{
    'name': "San Miguel - Prestamos",

    'summary': """
        San Miguel - Prestamos""",

    'description': """
        Manejo de Prestamos Empleados
        Manejo de Prestamos Clientes
        Manejo de Prestamos Por Pagar
    """,

    'author': "Warren Castro",
    'website': "http://www.recicladorasanmiguel.com.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'cierre_caja', 'purchase', 'hr'],

    # always loaded
    'data': [
        'views/prestamo.xml',      
        'views/purchase_order.xml',
        'views/report_abono.xml',
        'prestamos_report.xml' 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}
