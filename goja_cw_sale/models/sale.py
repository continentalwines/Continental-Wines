from odoo import models, fields, api
import pytz
from datetime import datetime, time

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commitment_date_only = fields.Date(
        string="Delivery Date (Date)",
        compute="_compute_commitment_date_only",
        search="_search_commitment_date_only",
        store=False
    )

    @api.depends("commitment_date")
    def _compute_commitment_date_only(self):
        tz_name = self.env.user.tz or 'UTC'
        user_tz = pytz.timezone(tz_name)
        for rec in self:
            if rec.commitment_date:
                utc_dt = pytz.utc.localize(rec.commitment_date.replace(tzinfo=None))
                rec.commitment_date_only = utc_dt.astimezone(user_tz).date()
            else:
                rec.commitment_date_only = False

    def _search_commitment_date_only(self, operator, value):
        if not value:
            return []
        
        # Get the CURRENT user's timezone
        tz_name = self.env.user.tz or 'UTC'
        user_tz = pytz.timezone(tz_name)

        # Convert picked date to UTC range
        date_start = user_tz.localize(
            datetime.combine(fields.Date.from_string(value), time.min)
        ).astimezone(pytz.utc).replace(tzinfo=None)

        date_end = user_tz.localize(
            datetime.combine(fields.Date.from_string(value), time.max)
        ).astimezone(pytz.utc).replace(tzinfo=None)

        return [
            ('commitment_date', '>=', date_start),
            ('commitment_date', '<=', date_end),
        ]