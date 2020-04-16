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

        #Obtain the current purchase order id:
        purchase_order_id = self.id        
        #Object of model 'purchase.order.line':
        purchase_order_obj = self.env['purchase.order'].browse(purchase_order_id)               
        #Retrieve the ids of the relatives lines belonging to the main purchase order:
        purchase_order_lines = self.env['purchase.order.line'].search([('order_id', '=', purchase_order_id)])            
        
        #Obtain the currency of purchase order:
        currency = purchase_order_obj.search([('id', '=', purchase_order_id)]).currency_id.id

        #Validate if the currency of purchase order is not Mexican Peso (MXN):
        if currency != 33: #MXN has the id 33 in model res.currency                   
            #If the currency is different to MXN, perform conversion:
            sql_query = """SELECT rate FROM res_currency_rate WHERE id = %s;"""
            self.env.cr.execute(sql_query, (currency,))
            rate_aux = self.env.cr.fetchone()
            rate = rate_aux[0] #Store rate or conversion factor
            conversion_factor = 1 / rate             

        #Validation in order to avoid purchases when price unit is lesser than sale price:
        for value in purchase_order_lines.ids:
            #Retrieve "sale price" from table 'product.template':                   
            sql_query = """SELECT list_price FROM product_template WHERE id = %s;"""
            self.env.cr.execute(sql_query, (value,))
            sale_price_aux = self.env.cr.fetchone()
            sale_price = sale_price_aux[0]        

            #Conversion to Mexican Pesos (MXN) of sale price:
            if currency != 33:
                #It is necessary to calculate the new value of currency:
                sale_price = float(sale_price) * float(conversion_factor)
                                
            #Get price_unit of each line from purchase order line:
            price_unit = self.env['purchase.order.line'].search([('id', '=', value)]).price_unit 
            
            #Validate if sale_price is lesser than purchase price unit, then arise error:         
            if sale_price < price_unit:
                msg = _('The purchase price is superior than sales price')
                raise UserError(msg)
    
        return result



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