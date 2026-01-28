# -*- coding: utf-8 -*-
{
    'name': "biblioteca_gestion",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
    Módulo de gestión de la biblioteca Calíope.
    """,

    'author': "Arantxa-Wara",
    'website': "https://github.com/Nimbus-Develop",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/biblioteca_security.xml',
        'security/ir.model.access.csv',
        # Primero el menú raíz (prestamo_views.xml lo define)
        'views/prestamo_views.xml',
        # Dashboard de estadísticas (depende del menú raíz)
        'views/dashboard_views.xml',
        # Luego catálogo (define menu_biblioteca_catalogo)
        'views/categoria_views.xml',
        # Después los que dependen de catálogo
        'views/libro_views.xml',
        'views/autor_views.xml',
        'views/views.xml',
        'views/templates.xml',
        # Informes
        'report/prestamo_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

