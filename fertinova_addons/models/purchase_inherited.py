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

        #Auxiliar variables:
        msg = ""
        prod_tmpl_obj = self.env['product.template']        
        pur_ord_lin_obj = self.env['purchase.order.line']

        #Instance of purchase order lines:
        purchase_order_lines = pur_ord_lin_obj.search([('order_id', '=', self.id)])
        
        #Validate if the currency of purchase order is not Mexican Peso (MXN):
        #mxn = self.env.ref('base.MXN')
        currency_of_company = self.env['res.company'].search([('id', '=', self.company_id.id)]).currency_id.id

        if currency_of_company != self.currency_id.id: 
            #If the currency is different to MXN, perform conversion:
            rate = self.env['res.currency.rate'].search([('id', '=', self.currency_id.id)]).rate              
                #Query for retrieve rate:            
                #sql_query = """SELECT rate FROM res_currency_rate WHERE id = %s;"""
                #self.env.cr.execute(sql_query, (self.currency_id.id,))
                #rate_aid = self.env.cr.fetchone()
                #rate_aux = rate_aid[0] 
                #_logger.info("\n\n\n\n rate_aux: %s", rate_aux)            
            conversion_factor = 1 / rate               
        
        #for value in self.order_line.filtered("product_id.product_tmpl_id.valid_price_unit"):
        for value in purchase_order_lines.ids:
            #Retrieve "sale price", "valid_price_unit", "product_name" from table 'product.template' considering product_id: 
            product_id = pur_ord_lin_obj.search([('id', '=', value)]).product_id.id

            sale_price       = prod_tmpl_obj.search([('id', '=', product_id)]).list_price 
            valid_price_unit = prod_tmpl_obj.search([('id', '=', product_id)]).valid_price_unit
            product_name     = prod_tmpl_obj.search([('id', '=', product_id)]).name

            #Validate if checkbox in product.template is True in order to proceed:
            if valid_price_unit == True:
                #Conversion to Mexican Pesos (MXN) of sale price:
                if currency_of_company != self.currency_id.id: 
                    #It is necessary to calculate the new value of currency:  
                    sale_price = float(sale_price) * float(conversion_factor)                   

                #Get price_unit of each line from purchase order line:
                price_unit = pur_ord_lin_obj.search([('id', '=', value)]).price_unit            

                #Validation in order to avoid purchases when price unit is lesser than sale price:
                if float(price_unit) > sale_price:
                    msg += _('\nThe purchase price of the product %s $%s is superior than sales price $%s\n') % (product_name, price_unit, sale_price)
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