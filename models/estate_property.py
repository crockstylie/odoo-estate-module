from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of the Estate Duh !!!"
    _order = "id desc"
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

    def _default_date_availability(self):
        return fields.Date.context_today(self) + relativedelta(months=3)

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date(
        string='Available from',
        default=lambda self: self._default_date_availability(),
        copy=False
    )
    expected_price = fields.Float(
        string='Expected price',
        required=True
    )
    selling_price = fields.Float(
        string='Selling price',
        copy=False,
        readonly=True
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
        ]
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
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        readonly=True,
        copy=False)
    property_tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    property_offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Property Offers')

    total_area = fields.Integer(
        string="Total area (m2)",
        compute="_compute_total_area",
        readonly=True)
    best_price = fields.Float(compute="_compute_best_price", readonly=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

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

    @api.constrains('expected_price', 'selling_price')
    def _check_price_difference(self):
        for prop in self:
            if (
                not float_is_zero(prop.selling_price, precision_rounding=0.01)
                and float_compare(prop.selling_price, prop.expected_price * 0.9, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price"
                )

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("canceled properties cannot be sold.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Sold properties cannot be canceled.")
        return self.write({"state": "canceled"})
