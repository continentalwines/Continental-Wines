from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    business_group = fields.Many2one(
        comodel_name='business.group',
        string='Custom Group',
        readonly=True,
    )
    business_channel = fields.Many2one(
        comodel_name='business.channel',
        string='Customer Channel',
        readonly=True,
    )

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['business_group'] = 'partner.business_group'
        res['business_channel'] = 'partner.business_channel'
        return res

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += ', partner.business_group, partner.business_channel'
        return res
