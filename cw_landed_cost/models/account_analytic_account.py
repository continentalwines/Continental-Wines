from odoo import models, api, fields

class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    customer_tags_ids = fields.Many2many('res.partner.category')