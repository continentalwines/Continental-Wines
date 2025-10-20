from odoo import _, api, fields, models

class ProductProcelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    goja_type = fields.Selection(string='Selected Type', selection=[('Wholesale', 'Wholesale'), ('By bottle', 'By bottle'),('Pouring', 'Pouring')])

    # x_type = fields.Selection(string='Selected Type', selection=[('Wholesale', 'Wholesale'), ('By bottle', 'By bottle'),('Pouring', 'Pouring')])
    
    
    
    
    