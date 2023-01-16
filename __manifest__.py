{
    'name': 'Combiwood Barkevik Factoringe',
    'version': '16.0.1.0',
    'category': 'Customization/Accounting',
    'author': 'OdooPS',
    'summary': 'Extended module Combiwood Barkevik added factoring',
    'description': """[3109231] Combiwood Barkevik uses factoring on some of their customers.
                                    Factoring is illustrated in this factoring illustration:""",
    'depends': [
        'contacts',
        'sale_management',
        'account_accountant',
        'l10n_no',
        'documents'
    ],
    'data': [
        'report/debtor_file.xml',
        'report/invoice_file.xml',

        'data/document_folder.xml',
        'data/invoice_and_debtor_file.xml',

        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/res_partner_bank_views.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
}
