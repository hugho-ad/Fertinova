# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    #########################################################
    # MODEL FIELDS
    #########################################################
    validation_price_unit = fields.Boolean(string='Purchase Price Unit must not exceed to Sales Price', 
                                           store=True,
                                           translate=True)

    #########################################################
    # METHOD FIELDS
    #########################################################                                          

