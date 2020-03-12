# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class StockMove(models.Model):
    _inherit = 'stock.move'

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
    def _create_account_move_line(self, credit_account_id, debit_account_id, journal_id):
        '''This methods intends to modify the original biusiness logic of the
           _create_account_move_line method in file addons/stock_account/stock.py'''
        self.ensure_one()
        AccountMove = self.env['account.move']
        StockMove = self.env['stock.move']
        quantity = self.env.context.get('forced_quantity', StockMove.product_qty)
        quantity = quantity if StockMove._is_in() else -1 * quantity

        # Make an informative `ref` on the created account move to differentiate between classic
        # movements, vacuum and edition of past moves.
        ref = StockMove.picking_id.name
        if self.env.context.get('force_valuation_amount'):
            if self.env.context.get('forced_quantity') == 0:
                ref = 'Revaluation of %s (negative inventory)' % ref
            elif self.env.context.get('forced_quantity') is not None:
                ref = 'Correction of %s (modification of past move)' % ref

        move_lines = self.with_context(forced_ref=ref)._prepare_account_move_line(quantity, abs(StockMove.value), credit_account_id, debit_account_id)
        if move_lines:
            date = self._context.get('force_period_date', fields.Date.context_today(self))
            new_account_move = AccountMove.sudo().create({
                'journal_id': journal_id,
                'line_ids': move_lines,
                'date': date,
                'ref': ref,
                'stock_move_id': StockMove.id,
                'analytic_account_id': self.analytic_account_id
            })
            new_account_move.post() 
        return super(StockMove.StockMove, self)._create_account_move_line()