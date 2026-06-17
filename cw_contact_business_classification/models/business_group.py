from odoo import fields, models


class BusinessGroup(models.Model):
    _name = 'business.group'
    _description = 'Business Group'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'A Business Group with this name already exists.'),
    ]
