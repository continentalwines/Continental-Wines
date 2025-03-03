{
    "name": "CW - Custom Landed Cost",
    "author": "Goja Solutions",
    "website": "https://www.gojasolutions.com/",
    "category": "Sales",
    "license": "AGPL-3",
    "summary": "Custom Landed Cost",
    "description": """Custom Landed Cost.""",
    "version": "16.0.1.0.0",
    'depends': ['sale','account','stock_landed_costs'],
    "data": [
        'views/account_analytic_account_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
