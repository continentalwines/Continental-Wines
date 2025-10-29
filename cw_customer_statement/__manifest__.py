{
    "name": "CW - Customer Statement",
    "author": "Goja Solutions",
    "category": "Accounting/Accounting",
    "license": "AGPL-3",
    "summary": "Report Customer Statement",
    "description": """Report Customer Statement.""",
    "version": "18.0.1.0.0",
    'depends': ['account_reports', 'sale'],
    "data": [
        'views/res_partner_views.xml',
        'reports/paperformat.xml',
        'reports/report_customer_statement.xml',
        'reports/report_multi_customer_statement.xml'
    ],
    'installable': True,
    'auto_install': False,
}
