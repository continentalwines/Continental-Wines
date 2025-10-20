from odoo import _, api, fields, models

class WineType(models.Model):
    _name = 'x_wine_type'
    _description = 'Wine Type'

    x_name = fields.Char()
    
    
    