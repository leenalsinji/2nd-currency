{
    'name': 'Accounting Secondary Currency',
    'version': '1.0',
    'category': 'Accounting',
    'depends': ['account','account_reports','account_asset'],
    'data': [
        'data/account_report_journal_audit.xml',
        'views/account_move_view.xml',
        'views/res_company_view.xml',
        'views/account_asset.xml',
    ],
    'installable': True,
    'application': True,
}