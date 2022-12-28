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
        'views/res_partner_inherit_view.xml',
        'views/sale_order_inherit_form.xml',
        'views/account_move_inherit_view.xml',
        'views/res_config_settings_views_combiwood_barkevik_factoring.xml',
        'views/res_partner_bank_inherit_form.xml',
        # 'views/shop_views.xml',
        # 'data/data.xml',

    ],
    'demo': [],
    'sequence': -200,
    'application': True,
    'installable': True,
    'auto_install': False,
}
