# -*- coding: utf-8 -*-
{
    'name': "hhd_cost_recovery",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board', 'account', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/hhd_invoice_wizard.xml',
        'wizard/hhd_invoice_button.xml',
        'wizard/wizard.xml',
        'views/chiphi.xml',
        'wizard/wizardreport.xml',
        'views/nhanvien.xml',
        'views/hoadon.xml',
        'report/report.xml',
        'views/mail.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}