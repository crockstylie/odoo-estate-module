{
    "name": "Odoo Estate Tutorial",
    "version": "0.1",
    "category": "Real Estate",
    "website": "https://github.com/crockstylie/odoo-estate-module",
    "author": "Crock",
    "license": "LGPL-3",
    "depends": [
        'base'
    ],
    "data": [
        'security/ir.model.access.csv',

        'views/estate_property_views.xml',
        'views/estate_menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
