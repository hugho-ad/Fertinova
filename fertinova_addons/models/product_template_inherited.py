# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #########################################################
    # MODEL FIELDS
    #########################################################
    valid_price_unit = fields.Boolean(string='Purchase Price Unit must not exceed to Sale Price')git 



    #########################################################
    # METHOD FIELDS
    ######################################################### 
