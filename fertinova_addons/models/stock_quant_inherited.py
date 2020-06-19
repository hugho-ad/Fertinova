# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)

#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET 107 DEVELOPED BY SEBASTIAN MENDEZ -- START
#//////////////////////////////////////////////////////////////////////////////////////////////#

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_view_stock_moves(self):
        """This method intends to extend the original method "action_view_stock_moves()" in order to pass the location_id selected in "stock.quant" by the context.
        This is made by entering into STOCK > MAIN DATA {Menu} > PRODUCTS {Menuitem} > a given product > Smart Button {action_open_quants}"""
        
        #Calling in order to extend method 'action_view_stock_moves':
        # HERE IS WHERE WE NEED PASS THE LOCATION
        
        # Hugho-ad Code:
        # Try this option:
        action = super(StockQuant, self.with_context(location_id=self.location_id.id)).action_view_stock_moves()
        # Or this:
        ctx = eval(action.get('context'))
        ctx.update({'location_id': self.location_id.id})
        action['context'] = str(ctx)
        # End Hugho-ad Code:

        #Add location_id into the context:
        self = self.with_context(location_id=self.location_id.id)  
        _logger.info('\n\n\n\n contexto en stock.quant: %s\n\n', str(self.env.context))        

        return action

#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET 107 DEVELOPED BY SEBASTIAN MENDEZ -- END
#//////////////////////////////////////////////////////////////////////////////////////////////#
