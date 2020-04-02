# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'analytic.acc.tag.wizard'
    _description = "Wizard for adding analytic accounts and labels"

    #########################################################
    # MODEL FIELDS
    #########################################################
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Analytic Account',
                                          store=True,
                                          translate=True) 

    analytic_tag_id = fields.Many2one('account.analytic.tag', 
                                      string='Analytic Tag',
                                      store=True,
                                      translate=True)



    #########################################################
    # MODEL METHODS
    #########################################################
    def accept_button(self):
        """This method intends to update analytic accounts and tags from a custommed wizard"""
        #Retrieve "id" of "move_id" for determining which analytic accounts and tags to update:
        move_id = self.env.context.get('active_id')   

        #Invoke method "button_cancel()" in order to cancel journal entry:
        account_move = self.env['account.move'].browse(move_id) #AccountMove object
        account_move.button_cancel()

        #Modify the analytic accounts and tags:
        dict_val = {
            'analytic_account_id': self.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_id.ids)]
        }

        #Retrieval of code from model 'account.account' matching with account_id:            
        sql_query = """SELECT code FROM account_account WHERE id = %s;"""
        self.env.cr.execute(sql_query, (move_id,))
        code = self.env.cr.fetchone()
        code_aux = code[0]               

        #Iterate to create/update analytic accounts and tags into field 
        #line_ids One2Many with the new values:
        for line in account_move.line_ids:
            #Validate that accounts belonging to Equity, Assets and Liabilities 
            #must not be considered:
            if code_aux[0] not in [1, 2 , 3]: 
                line.write(dict_val)
        
        #Invoke method "post()" in order to post the journal entry:            
        account_move.post()