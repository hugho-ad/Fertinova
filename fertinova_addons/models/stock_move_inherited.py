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
                                          index=True, 
                                          store=True, 
                                          translate=True
                                         )                               


    #########################################################
    # MODEL METHODS
    #########################################################
    def _generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id):
        """This method intends to add the value of analytic account 
           from Tranfers into account journal"""
        
        #Retrieve original dictionary:        
        res = super(StockMove, self)._generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id)

        #Update the value of analytic account in credit and debit lines:
        
        #self.debit_line_vals = {'analytic_account_id': self.analytic_account_id}
        #self.credit_line_vals = {'analytic_account_id': self.analytic_account_id}
        
        res = super()._generate_valuation_lines_data(self, partner_id, qty, debit_value, credit_value, debit_account_id, credit_account_id)
        res['debit_line_vals'].update({'analytic_account_id': self.analytic_account_id.id})
        res['credit_line_vals'].update({'analytic_account_id': self.analytic_account_id.id})
        
        #self._debit_line_vals.write({'analytic_account_id': self.analytic_account_id})
        #self._credit_line_vals.write({'analytic_account_id': self.analytic_account_id})
        
        return res
