# Copyright 2019 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    accounting_date = fields.Date(
        string='Force Accounting Date',
        help="Date at which the accounting entries will be created"
        " in case of automated product in picking.  If empty, the "
        "stock picking date will be used.")

    @api.multi
    def action_done(self):
        """Inherit method to add for context the accounting_date in the
        account_entry and change the debit and credit quantity for each entry
        created, if the accounting_date field is set."""
        with_acc_date = self.filtered('accounting_date')
        wo_acc_date = self - with_acc_date
        res = super(Picking, wo_acc_date).action_done()
        for picking in with_acc_date:
            res = super(Picking, picking.with_context(
                force_period_date=picking.accounting_date)).action_done()
            move_purchase = picking.move_lines.filtered(
                lambda move: move.purchase_line_id)
            for move in move_purchase:
                unit_price = move.purchase_line_id.price_unit
                company_currency = picking.company_id.currency_id

                if (move.purchase_line_id.currency_id != company_currency):
                    unit_price = move.purchase_line_id.currency_id._convert(
                        unit_price, company_currency,
                        picking.company_id, picking.accounting_date)

                account_moves = move.account_move_ids
                cost = move.product_qty * unit_price
                account_moves.button_cancel()
                for account_move in account_moves:
                    debit_move_line = account_move.line_ids.filtered(
                        lambda move_line: move_line.debit > 0)
                    debit_move_line.with_context(
                        check_move_validity=False).write({
                            'debit': cost
                            })
                    credit_move_line = account_move.line_ids.filtered(
                        lambda move_line: move_line.credit > 0)
                    credit_move_line.with_context(
                        check_move_validity=False).write({
                            'credit': cost
                            })
                account_moves.post()
        return res
