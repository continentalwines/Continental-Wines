from odoo import _, api, fields, models

class Region(models.Model):
    _name = 'x_region'
    _description = 'Region'

    x_name = fields.Char()
    x_country_id = fields.Many2one('res.country', string='Country')
    
    