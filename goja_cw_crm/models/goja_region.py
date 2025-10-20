from odoo import _, api, fields, models

class GojaRegion(models.Model):
    _name = 'goja.region'
    _description = 'Region'

    name = fields.Char()
    country_id = fields.Many2one('res.country', string='Country')
    
    