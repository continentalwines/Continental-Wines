from odoo import models, fields, api, _
from datetime import datetime


class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_inv_po_number(self, field_name=''):
        self.ensure_one()
        if not field_name:
            return self.ref
        source_orders = self.line_ids.sale_line_ids and \
            self.line_ids.sale_line_ids.order_id or False
        if source_orders:
            for order_dict in source_orders.read():
                if order_dict.get(field_name):
                    return order_dict.get(field_name)
        return self.ref