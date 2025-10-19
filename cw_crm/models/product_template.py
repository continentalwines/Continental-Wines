from odoo import _, api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    region_id = fields.Many2one(comodel_name='goja.region')
    country_id = fields.Many2one(comodel_name='res.country')
    wine_type_id = fields.Many2one('wine.type')
    other_notes = fields.Text(string='Other Notes')
    price_by_bottle = fields.Float(string='Price (By Bottle)')
    price_pouring = fields.Float(string='Price (Pouring)')


    x_region_id = fields.Many2one(comodel_name='x_region')
    x_country_id = fields.Many2one(comodel_name='res.country')
    x_wine_type_id = fields.Many2one('x_wine_type')
    x_other_notes = fields.Text(string='Other Notes')
    x_price_by_bottle = fields.Float(string='Price (By Bottle)')
    x_price_pouring = fields.Float(string='Price (Pouring)')
    
    
    
    