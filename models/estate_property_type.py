from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _sql_constraints = [
        (
            'check_name',
            'UNIQUE(name)',
            'The type name must be unique.'
        )
    ]

    name = fields.Char(
        string='Name',
        required=True
    )
