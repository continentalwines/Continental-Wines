# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Continental Wines CRM',
    'category': 'Custom',
    "author": "Goja Solutions",
    "version": "18.0.1.0.0",
    'description': """
    """,
    'depends': [
    	'crm',
    	'sale_management',
        'stock'
        'sale_crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'actions/server_actions.xml',
        'views/region.xml',
        'views/wine_type.xml',
        'views/product_template.xml',
        'views/product_pricelist.xml',
        'views/crm_lead.xml',
        'views/menu.xml',
    ],
    'license': 'OEEL-1',
}
