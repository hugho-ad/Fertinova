# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class Sale_Line_Inherited(models.Model):
    _inherit = 'sale.order.line'

    #########################################################
    # MODEL FIELDS
    #########################################################
    qty_to_deliver = fields.Float(string='Quantity_to_deliver', 
                                  digits=dp.get_precision('Product Unit of Measure'), 
                                  compute='_get_qty_to_deliver',
                                  store=True,
                                  translate=True
                                 )

    #########################################################
    # MODEL METHODS
    #########################################################
    @api.depends('product_uom_qty', 'qty_delivered')
    def _get_qty_to_deliver(self):
        '''This method computes the difference between product on demand and quantity delivered'''
        for rec in self:
            if not rec.product_uom_qty and rec.qty_delivered:
                rec.qty_to_deliver= 0.0
            else:
                rec.qty_to_deliver = rec.product_uom_qty - rec.qty_delivered