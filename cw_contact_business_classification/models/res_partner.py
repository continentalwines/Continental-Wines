from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    business_group = fields.Many2one(
        comodel_name='business.group',
        string='Group',
        compute='_compute_business_group',
        inverse='_inverse_business_group',
        store=True,
    )
    business_channel = fields.Many2one(
        comodel_name='business.channel',
        string='Channel',
        compute='_compute_business_channel',
        inverse='_inverse_business_channel',
        store=True,
    )

    @api.depends('parent_id', 'parent_id.business_group')
    def _compute_business_group(self):
        for record in self:
            if record.parent_id:
                record.business_group = record.parent_id.business_group

    def _inverse_business_group(self):
        pass  # stored field — value is written directly by the ORM for top-level contacts

    @api.depends('parent_id', 'parent_id.business_channel')
    def _compute_business_channel(self):
        for record in self:
            if record.parent_id:
                record.business_channel = record.parent_id.business_channel

    def _inverse_business_channel(self):
        pass  # stored field — value is written directly by the ORM for top-level contacts
