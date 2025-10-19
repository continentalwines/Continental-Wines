from odoo import _, api, fields, models

class CrmLeadLine(models.Model):
    _name = 'crm.lead.line'
    _description = 'Lead Line'

    sequence = fields.Integer(string='Sequence')
    crm_opportunity_id = fields.Many2one('crm.lead', string='Lead/Opportunity')
    product_template_id = fields.Many2one('product.template', string='')
    region_id = fields.Many2one(comodel_name='goja.region', string='Region')
    country_id = fields.Many2one(comodel_name='res.country', string='Country')
    price_wholesale = fields.Float(string='Price (Wholesale)')
    price_by_bottle = fields.Float(string='Price (By Bottle)')
    price_pouring = fields.Float(string='Price (Pouring)')
    type_selected = fields.Selection(string='Selected Type', selection=[('Wholesale', 'Wholesale'), ('By bottle', 'By bottle'),('Pouring', 'Pouring')])
    notes = fields.Text(string='Internal Notes')

    @api.onchange('product_template_id')
    def onchange_price(self):
        if self.product_template_id:
                self.price_wholesale =self.product_template_id.list_price,
                self.price_by_bottle=self.product_template_id.price_by_bottle,
                self.price_pouring=self.product_template_id.price_pouring,
    
    
    