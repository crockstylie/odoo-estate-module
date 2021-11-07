import datetime

from odoo import fields, models, api
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
        required=True
    )
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')
    total_area = fields.Float(compute="_compute_total_area", readonly=True)
    best_price = fields.Float(compute="_compute_best_price", readonly=True)

    @api.depends("living_area", "garden", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.property_offer_ids.mapped("price")) if prop.property_offer_ids else 0.0
