# Copyright 2019 Vauxoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.depends('qty_delivered', 'qty_to_invoice', 'qty_invoiced')
    def _compute_subtotal_qtys(self):
        for line in self:
            line.subtotal_qty_to_invoice = (line.price_unit *
                                            line.qty_to_invoice)
            line.subtotal_qty_delivered = line.price_unit * line.qty_delivered
            line.subtotal_qty_invoiced = line.price_unit * line.qty_invoiced

    subtotal_qty_to_invoice = fields.Monetary(
        'Sub. Qty. to Invoice', compute='_compute_subtotal_qtys',
        readonly=True, store=True)

    subtotal_qty_delivered = fields.Monetary(
        'Sub. Qty. Delivered', compute='_compute_subtotal_qtys',
        readonly=True, store=True)

    subtotal_qty_invoiced = fields.Monetary(
        'Sub. Qty. Invoiced', compute='_compute_subtotal_qtys',
        readonly=True, store=True)
