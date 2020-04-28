# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.translate import _      


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    ##########################################################
    # MODEL METHODS
    ##########################################################
    @api.multi
    def button_confirm(self):
        """This method obtain the purchase order id and its lines, in order to get
           sale prices of those products and avoiding to acquire when this cost
           is lesser than company wants to purchase from providers"""
        result = super(PurchaseOrder, self).button_confirm()   
                   
        #Validate if the currency of purchase order is not Mexican Peso (MXN):
        mxn = self.env.ref('base.MXN')
        if self.currency_id != mxn.id:                  
            #If the currency is different to MXN, perform conversion:
            rate = mxn._get_conversion_rate(self.env.user.company_id.currency_id, self.currency_id, self.company_id, self.date_order)           

        msg = ""
        for value in self.order_line.filtered("product_id.product_tmpl_id.valid_price_unit"):
            #Auxiliar variables:
            price_unit = value.price_unit * rate
            sale_price = value.product_id.list_price
            #Validation in order to avoid purchases when price unit is lesser than sale price:
            if sale_price <= price_unit:
                msg += _('\nThe purchase price $%s is superior than sales price $%s\n') % (price_unit, sale_price)
        
        if not msg:
            return result
        
        raise UserError(msg)



class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    #########################################################
    # MODEL FIELDS
    #########################################################
    qty_to_receive = fields.Float(string='Quantity to receive', 
                                  digits=dp.get_precision('Product Unit of Measure'), 
                                  compute='_get_qty_to_receive',
                                  store=True,
                                  translate=True)

    ##########################################################
    # MODEL METHODS
    ##########################################################
    @api.depends('product_qty', 'qty_received')
    def _get_qty_to_receive(self):
        '''This method computes the difference between product quantity and quantity received'''
        for rec in self:
            if not rec.product_qty and rec.qty_received:
                rec.qty_to_receive = 0.0
            else:
                rec.qty_to_receive = rec.product_qty - rec.qty_received