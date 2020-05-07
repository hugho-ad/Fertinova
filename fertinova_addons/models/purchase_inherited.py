# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.translate import _    


#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 035    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
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
        #Call of Odoo Standard Method "button_confirm":
        result = super(PurchaseOrder, self).button_confirm() 

        #Instance of purchase order lines:
        purchase_order_lines = self.env['purchase.order.line'].search([('id', '=', self.order_id.id)])
        
        #Validate if the currency of purchase order is not Mexican Peso (MXN):
        mxn = self.env.ref('base.MXN')
        if self.currency_id.id != mxn.id: 
            #If the currency is different to MXN, perform conversion:
            rate = self.env['res.currency.rate'].search([('id', '=', self.currency_id.id)]).rate
            conversion_factor = 1 / rate
        
        msg = ""
        #for value in self.order_line.filtered("product_id.product_tmpl_id.valid_price_unit"):
        for value in purchase_order_lines.ids:
            #Retrieve "sale price" from table 'product.product' considering product_id: 
            product_id = self.env['purchase.order.line'].search([('id', '=', value)]).product_id.id
            sale_price = self.env['product.template'].search([('id', '=', product_id)]).list_price 

            #Conversion to Mexican Pesos (MXN) of sale price:
            if self.currency_id != mxn.id: 
                #It is necessary to calculate the new value of currency:  
                sale_price = float(sale_price) * float(conversion_factor)

            #Get price_unit of each line from purchase order line:
            price_unit = self.env['purchase.order.line'].search([('id', '=', value)]).price_unit               

            #Validation in order to avoid purchases when price unit is lesser than sale price:
            if float(price_unit) > sale_price:
                msg += _('\nThe purchase price $%s is superior than sales price $%s\n') % (price_unit, sale_price)
            #If everything is OK, proceed with purchase order confirmation
            if not msg:
                return result
            
            raise UserError(msg)       
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 035    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#




#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
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
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  