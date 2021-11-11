from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of the Estate Duh !!!"
    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            'The expected price must be strictly positive.'
        ),
        (
            'check_selling_price',
            'CHECK(selling_price >= 0)',
            'The selling price must be positive.'
        )
    ]

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string='Availability date',
        copy=False,
        default=fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(
        string='Expected price',
        required=True
    )
    selling_price = fields.Float(
        string='Selling price',
        readonly=True,
        copy=False
    )
    bedrooms = fields.Integer(
        string='Bedrooms',
        default=2
    )
    living_area = fields.Integer('Living area (m2)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden area (m2)')
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
        string='Status',
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
    user_id = fields.Many2one(
        "res.users",
        string="Salesman",
        readonly=True,
        copy=False,
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')
    total_area = fields.Integer(
        string="Total area (m2)",
        compute="_compute_total_area",
        readonly=True)
    best_price = fields.Float(compute="_compute_best_price", readonly=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price = max(prop.property_offer_ids.mapped("price")) if prop.property_offer_ids else 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
