from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    customer_reference = fields.Char(related='order_id.client_order_ref', store=True, index=True, string="Customer Reference")
    delivery_address = fields.Char(related='order_id.partner_shipping_id.display_name', store=True, index=True, string="Delivery Address")
