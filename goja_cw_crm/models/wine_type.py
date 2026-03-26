from odoo import _, api, fields, models

class WineType(models.Model):
    _name = 'wine.type'
    _description = 'Wine Type'
    _order = 'sequence, name'

    name = fields.Char()
    sequence = fields.Integer(default=10)
    
    
    