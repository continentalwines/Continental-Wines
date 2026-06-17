{
    'name': 'Contact Business Classification',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'license': 'LGPL-3',
    'summary': 'Add Group and Channel classification to contacts with parent inheritance',
    'author': 'Goja Solutions',
    'depends': ['contacts', 'sales_team', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/business_group_views.xml',
        'views/business_channel_views.xml',
        'views/res_partner_views.xml',
        'views/sale_order_line_views.xml',
        'views/sale_report_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False,
}
