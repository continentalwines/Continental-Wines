from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    business_group = fields.Many2one(
        comodel_name='business.group',
        string='Custom Group',
        related='order_partner_id.business_group',
        store=True,
    )
    business_channel = fields.Many2one(
        comodel_name='business.channel',
        string='Customer Channel',
        related='order_partner_id.business_channel',
        store=True,
    )
