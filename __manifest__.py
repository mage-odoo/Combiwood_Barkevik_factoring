{
    'name': 'Combiwood Barkevik Factoringe',
    'version': '1.1.0',
    'category': 'extended module of Combiwood',
    'author': 'manthan',
    'summary': 'Extended module Combiwood Barkevik added factoring',
    'description': """Combiwood Barkevik uses factoring on some of their customers.
                                    Factoring is illustrated in this factoring illustration:""",
    'depends': ['base', 'account', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/invoice_file.xml',
        'data/debtor_file.xml',
        'data/account_move_sequence.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_inherit_view.xml',
        'views/sale_order_inherit_form.xml',
        'views/account_move_inherit_view.xml',
        'views/res_partner_bank_inherit_form.xml',
    ],
    'demo': [],
    'sequence': -200,
    'application': True,
    'installable': True,
    'auto_install': False,
}
