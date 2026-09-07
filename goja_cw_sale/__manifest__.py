# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Continental Wines Sale',
    'category': 'Custom',
    "author": "Goja Solutions",
    "version": "18.0.1.0.0",
    'description': """
    """,
    'depends': [
        'base',
    	'sale_management',
    	'sale_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_views.xml',
        'views/cw_orphan_move_views.xml',
    ],
    'license': 'OEEL-1',
}
