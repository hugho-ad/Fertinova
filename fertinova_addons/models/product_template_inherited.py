# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
_logger = logging.getLogger(__name__) 


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #########################################################
    # MODEL FIELDS
    #########################################################
    valid_price_unit = fields.Boolean(string='Purchase Price Unit must not exceed to Sale Price', 
                                      store=True,
                                      translate=True)



    #########################################################
    # METHOD FIELDS
    ######################################################### 
    @api.onchange('valid_price_unit')
    def checking_valid_price_unit(self):
        """This method intends to check up checkboxes in models 
           'product.template' & 'product.product' """
        #Retrieve current id:
        product_id = self._origin.id

        #If in model product
        if self.valid_price_unit == True:
            validation_price_unit = self.env['product.product'].search([('id', '=', product_id)]).validation_price_unit
            validation_price_unit = True

        if self.valid_price_unit == False:
            validation_price_unit = self.env['product.product'].search([('id', '=', product_id)]).validation_price_unit
            validation_price_unit = False
            

