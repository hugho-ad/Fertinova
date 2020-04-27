# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__) 


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
    @api.onchange('validation_price_unit')
    def checking_valid_price_unit(self):
        """This method intends to check up the checkboxes in models 
           'product.template' & 'product.product' """
        #Retrieve current id:
        product_id = self._origin.id

        #If in model product
        if self.validation_price_unit == True:
            valid_price_unit = self.env['product.template'].search([('id', '=', product_id)]).valid_price_unit
            valid_price_unit = True 

        if self.validation_price_unit == False:
            valid_price_unit = self.env['product.template'].search([('id', '=', product_id)]).valid_price_unit
            valid_price_unit = False
                                               