# -*- coding: utf-8 -*-
{
    'name': "crm_customer_request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm', 'product', 'sale_management'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'wizard/crm_lead_excel_view.xml',
        'views/quotation_view.xml',
        'views/crm_lead_inherit.xml',
        'views/crm_lead_form.xml',
        'views/customer_request.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
