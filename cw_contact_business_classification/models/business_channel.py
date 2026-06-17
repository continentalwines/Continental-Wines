from odoo import fields, models


class BusinessChannel(models.Model):
    _name = 'business.channel'
    _description = 'Business Channel'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A Business Channel with this name already exists.'),
    ]
