# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import logging
_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    insect_type = fields.Char(string="Insect type")
    nest_location = fields.Char(string="Nest location")
    situation_details = fields.Text(string="Situation description")
    already_came = fields.Boolean(string="Already came")
    already_came_date = fields.Date(string="Already came date")
    notes = fields.Text(string="Additional information")

    
    

    