{
    'name': 'Combiwood Barkevik Factoringe',
    'version': '1.1.0',
    'category': 'extended module of Combiwood',
    'author': 'manthan',
    'summary': 'Extended module Combiwood Barkevik added factoring',
    'description': """Combiwood Barkevik uses factoring on some of their customers.
                                    Factoring is illustrated in this factoring illustration:""",
    'depends': ['base', 'account_accountant', 'sale_management', 'contacts'],  # 'l10n_no',
    'data': [
        # 'security/ir.model.access.csv',
        'data/document_folder.xml',
        'data/invoice_and_debtor_file.xml',
        'data/account_move_sequence.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_inherit_view.xml',
        'views/sale_order_inherit_form.xml',
        'views/account_move_inherit_view.xml',
        'views/res_partner_bank_inherit_form.xml',
        'views/res_company_view.xml',
        'report/deptor.xml',
        # 'report/invoice.xml'
    ],
    'demo': [],
    'sequence': -200,
    'application': True,
    'installable': True,
    'auto_install': False,
}
