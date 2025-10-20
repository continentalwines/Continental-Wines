from odoo import _, api, fields, models

class WineType(models.Model):
    _name = 'wine.type'
    _description = 'Wine Type'

    name = fields.Char()
    
    
    