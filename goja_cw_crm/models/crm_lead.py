from odoo import _, api, fields, models
from odoo.exceptions import UserError



class CrmLead(models.Model):
    _inherit = 'crm.lead'

    agreed_pricelist_id = fields.Many2one(comodel_name='product.pricelist')
    crm_lead_line_ids = fields.One2many(comodel_name='crm.lead.line', inverse_name='crm_opportunity_id', string='CRM Lead Lines')
    quotation_date = fields.Date(string='Quotation Date')
    other_notes = fields.Text(string='Other Notes')
    blank_agreed_pricelist = fields.Boolean(related='agreed_pricelist_id.goja_is_blank_pricelist')

    @api.model_create_multi
    def create(self, vals_list):
        leads = super(CrmLead, self).create(vals_list)
        for lead in leads:
            if lead.partner_id and not lead.agreed_pricelist_id:
                lead.agreed_pricelist_id = lead.partner_id.property_product_pricelist
        return leads
        

    @api.onchange('partner_id')
    def onchange_partner_pricelist(self):
        if self.partner_id:
            self.agreed_pricelist_id = self.partner_id.property_product_pricelist

    def create_pricelist_from_crm(self):
        if self.partner_id.property_product_pricelist.goja_is_blank_pricelist:
            if self.crm_lead_line_ids:
                new_pricelist = self.env['product.pricelist'].create({
                        'name': self.partner_id.name + " Pricelist test",
                    })
                    
                self.partner_id.write({"property_product_pricelist": new_pricelist.id})
                self.agreed_pricelist_id = new_pricelist
                
                for line in self.crm_lead_line_ids:
                
                    if line.type_selected == "Wholesale":
                        line_price = line.price_wholesale
                    elif line.type_selected == "By bottle":
                        line_price = line.price_by_bottle
                    elif line.type_selected == "Pouring":
                        line_price = line.price_pouring
                    else:
                        line_price = 0
                    
                    if line_price > 0:
                    
                        self.env['product.pricelist.item'].create({
                                'pricelist_id': new_pricelist.id,
                                'applied_on': "1_product",
                                'product_tmpl_id': line.product_template_id.id,
                                'compute_price': "fixed",
                                'fixed_price': line_price,
                                'goja_type': line.type_selected
                            })

        else:
            raise UserError("This customer already has a custom pricelist!")
            
    def update_pricelist_from_crm(self):
        if not self.partner_id.property_product_pricelist.goja_is_blank_pricelist:
            if self.crm_lead_line_ids:
                pricelist = self.partner_id.property_product_pricelist
                changed_lines = 0
                
                for line in self.crm_lead_line_ids:
                
                    if line.type_selected == "Wholesale":
                        line_price = line.price_wholesale
                    elif line.type_selected == "By bottle":
                        line_price = line.price_by_bottle
                    elif line.type_selected == "Pouring":
                        line_price = line.price_pouring
                    else:
                        line_price = 0
                    
                    if line_price > 0:
                    
                        existing_line = self.env['product.pricelist.item'].search([
                                ['pricelist_id', '=', pricelist.id],
                                ['product_tmpl_id', '=', line.product_template_id.id]
                                # ['fixed_price', '!=', line_price]
                            ])
                        
                        if existing_line:
                            if existing_line.fixed_price != line_price:
                                existing_line.write({
                                        'fixed_price': line_price,
                                        'goja_type': line.type_selected
                                    })
                            
                                changed_lines = changed_lines + 1
                        
                        else:
                            self.env['product.pricelist.item'].create({
                                    'pricelist_id': pricelist.id,
                                    'applied_on': "1_product",
                                    'product_tmpl_id': line.product_template_id.id,
                                    'compute_price': "fixed",
                                    'fixed_price': line_price,
                                    'goja_type': line.type_selected
                                })
                        changed_lines = changed_lines + 1
                    
                if changed_lines == 0:
                    raise UserError("Nothing to update!")

        else:
            raise UserError("This customer doesn't have a custom pricelist yet!")
    
    
    
    
    