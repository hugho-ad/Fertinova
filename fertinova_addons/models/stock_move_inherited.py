# -*- coding: utf-8 -*-

import logging

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

_logger = logging.getLogger(__name__)


class StockMove(models.Model):
    _inherit = "stock.move"

    #########################################################
    # MODEL FIELDS
    #########################################################
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Analytic Account',
                                          store=True,
                                          translate=True)  

    analytic_tag_id = fields.Many2many('account.analytic.tag', 
                                       string='Analytic Tag',                                       
                                       store=True,
                                       translate=True)                                       



    #########################################################
    # MODEL METHODS
    #########################################################
    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
      """This method intends to expand the business logic in order to create into
         journal entry the new value of analytic accounts"""
      #Sample about what is inside the res in preparation method of journal entry:   
      #[
      # 0, 0, {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'credit': 235.0, 'debit': 0, 'account_id': 4}, 
      # 0, 0, {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'debit': 235.0, 'credit': 0, 'account_id': 6}
      #]     
            
      #Retrieve original list:
      res = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        
      #Creation of the list to be returned:
      result = []      
      #Iteration of res:
      for v in res:        
        #Obtain "account_id" from the original tuple from its internal dictionaty (0, 0, dict{}):
        account_id = v[2].get('account_id')  

        #Retrieval of "code" from model 'account.account' matching with account_id:                    
        code = self.env['account.account'].search([('id', '=', account_id)]).code         
                           
        #Assign and create the new value of analytic_account:           
        new_vals = v[2] #get the dictionary from original tuple (0, 0, dict{})
        
        #Validate that accounts belonging to Equity, Assets and Liabilities must not be considered: 
        if int(code[0]) not in [1, 2 , 3]:
          new_vals['analytic_account_id'] = self.analytic_account_id.id                    
          new_vals['analytic_tag_ids'] = [(6, 0, self.analytic_tag_id.ids)]

        #Append new values into original dictionary:
        element = (0, 0, new_vals)
        result.append(element) 
                            
      return result



class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    #########################################################
    # MODEL FIELDS
    #########################################################
    operative_qty = fields.Float(string='Operative Quantity', 
                                 digits=dp.get_precision('Product Unit of Measure'),
                                 compute='_get_operative_qty')      

    inputs = fields.Float(string='Inputs', 
                          digits=dp.get_precision('Product Unit of Measure')) 

    outputs = fields.Float(string='Outputs', 
                           digits=dp.get_precision('Product Unit of Measure'))     

    transfers = fields.Float(string='Transfers', 
                             digits=dp.get_precision('Product Unit of Measure')) 

    accumulated_qty = fields.Float(string='Accumulated Quantity', 
                                   digits=dp.get_precision('Product Unit of Measure'))                               

    price_unit = fields.Float(string='Price Unit', 
                              digits=dp.get_precision('Product Unit of Measure'), 
                              compute='_get_price_unit') 

    accumulated_ammount = fields.Float(string='Accumulated Ammount', 
                                       digits=dp.get_precision('Product Unit of Measure'))   

    calculated_average_cost = fields.Float(string='Calculated Average Cost', 
                                           digits=dp.get_precision('Product Unit of Measure'))   

    average_cost_difference = fields.Float(string='Average Cost Difference', 
                                           digits=dp.get_precision('Product Unit of Measure'))                                             
                                           
    #########################################################
    # MODEL METHODS
    #########################################################
    @api.model
    def _get_operative_qty(self):
      rows = self.env['stock.move.line'].search([])
      _logger.info('\n\n\n\n PRINTING ROWS: %s\n\n\n\n', rows)

      for val in self:
            _logger.info('\n\n\n\n PRINTING vals product: %s\n\n\n\n', vals.product_id.id)
            
      #rows_grouped_by_product = self.read_group(
      #  [([])],#Domain
      #  ['product_id'],#Fiels to access
      #  ['product_id.id']#group_by 
      #)
      #_logger.info('\n\n\n\n rows_grouped_by_product: %s\n\n\n\n', rows_grouped_by_product)

    def _get_inputs(self):
      pass

    def _get_outputs(self):
      pass
    
    def _get_transfers(self):
      pass

    def _get_accumulated_qty(self):
      pass

    def _get_price_unit(self):
      pass

    def _get_accumulated_ammount(self):
      pass

    def _get_calculated_average_cost(self):
      pass  

    def _get_average_cost_difference(self):
      pass                                  