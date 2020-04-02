# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    #########################################################
    # MODEL FIELDS
    #########################################################
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Analytic Account',
                                          store=True,
                                          translate=True
                                         )                           



    #########################################################
    # MODEL METHODS
    #########################################################
    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
        """This method intends to expand the business logic in order to create into
           journal entry the new value of analytic accounts"""
        #Sample about what is inside the res in preparation method of journal entry:   
          #[
          # {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'credit': 235.0, 'debit': 0, 'account_id': 4}, 
          # {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'debit': 235.0, 'credit': 0, 'account_id': 6}
          #]     
            
        #Retrieve original list:
        res = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        
        #Creation of the list to be returned:
        result = []
        
        #Iteration of res:
        for v in res:        
            #Obtain "account_id" from the original tuple (0, 0, dict{}):
            account_id = v[2].get('account_id')  
            
            #Retrieval of account_code from model 'account.account' matching with account_id:            
            sql_query = """SELECT code FROM account_account WHERE id = %s;"""
            self.env.cr.execute(sql_query, (account_id,))
            code = self.env.cr.fetchone()
            code_aux = code[0]
            
            #Validate that accounts belonging to Equity, Assets and Liabilities 
            #must not be considered:
            if code_aux[0] not in [1, 2 , 3]:
                #Assign and create the new value of analytic_account:
                new_account = v[2] #get the dictionary from original tuple (0, 0, dict{})
                new_account['analytic_account_id'] = self.analytic_account_id.id
                element = (0, 0, new_account)
                result.append(element)
            
        return result
