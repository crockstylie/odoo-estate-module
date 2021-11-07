import datetime

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of the Estate Duh !!!"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string='Availability date',
        copy=False,
        default=fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float('Expected price', required=True)
    selling_price = fields.Float(
        string='Selling price',
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2
    )
    living_area = fields.Integer('Living area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area')
    garden_orientation = fields.Selection(
        string='Garden orientation',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        help='Garden orientation is used to describe the garden orientation'
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        copy=False,
        default='new',
        required=True,
        help='Garden orientation is used to describe the garden orientation'
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
