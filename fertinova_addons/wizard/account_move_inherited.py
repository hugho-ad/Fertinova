# -*- coding: utf-8 -*-

import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__) 

class Wizard(models.TransientModel):
    _name = 'analytic.acc.tag.wizard'
    _description = "Wizard for adding analytic accounts and labels"

    #########################################################
    # MODEL FIELDS
    #########################################################
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Analytic Account', 
                                          index=True, 
                                          store=True, 
                                          translate=True
                                          #required=True
                                         )

    analytic_tag_id = fields.Many2one('account.analytic.tag', 
                                      string='Analytic Tag', 
                                      index=True, 
                                      store=True, 
                                      translate=True
                                      #required=True
                                     )

    #########################################################
    # MODEL METHODS
    #########################################################
    @api.model
    @api.multi
    def accept_button(self, args, *kwargs):
        """This method intends to update analytic accounts and tags from a custom wizard"""
        #Retrieve "id" of "move_id" for determining which analytic accounts and tags to update
        move_id = self.env.context.get('active_id')
        _logger.info('\n\n\nPRINTING THE SPECIFIC MOVE_ID \n%s\n', move_id)
                
        #Invoke method "button_cancel()" in order to cancel journal entry
        _logger.info('\n\n\nINTENDING TO CANCEL JOURNAL ENTRY\n')
        AccountMove = self.env['account.move'] #AccountMove object
        AccountMove.button_cancel()

        #Modify the analytic accounts and tags
        dict_val = {
            'analytic_account_id': self.analytic_tag_id.id,
            'analytic_tag_ids': self.analytic_tag_id.ids
        }
        _logger.info('\n\n\nINTENDING TO PRINT my_dict: \n%s', dict_val)
        AccountMove.write(1, move_id, dict_val)

        #Invoke method "action_post()" in order to post journal entry
        #_logger.info('\n\n\nINTENDING TO POST JOURNAL ENTRY')
        #AccountMove.action_post()