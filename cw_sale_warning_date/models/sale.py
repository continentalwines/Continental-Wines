from odoo import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('commitment_date', 'expected_date')
    def _onchange_commitment_date(self):
        """ Replace for not show warning """
        if self.commitment_date and self.expected_date and \
            self.commitment_date < self.expected_date:
            return {}
