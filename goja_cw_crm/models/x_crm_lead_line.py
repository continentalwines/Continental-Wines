from odoo import _, api, fields, models

class CrmLeadLine(models.Model):
    _name = 'x_crm_lead_line'
    _description = 'Lead Line'

    x_sequence = fields.Integer(string='Sequence')
    x_crm_opportunity_id = fields.Many2one('crm.lead', string='Lead/Opportunity')
    x_product_template_id = fields.Many2one('product.template', string='')
    x_region_id = fields.Many2one(comodel_name='goja.region', string='Region')
    x_country_id = fields.Many2one(comodel_name='res.country', string='Country')
    x_price_wholesale = fields.Float(string='Price (Wholesale)')
    x_price_by_bottle = fields.Float(string='Price (By Bottle)')
    x_price_pouring = fields.Float(string='Price (Pouring)')
    x_type_selected = fields.Selection(string='Selected Type', selection=[('Wholesale', 'Wholesale'), ('By bottle', 'By bottle'),('Pouring', 'Pouring')])
    x_notes = fields.Text(string='Internal Notes')

    
    
    