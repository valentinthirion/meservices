# -*- coding: utf-8 -*-

import logging
from openerp import http, _
from openerp.http import request

_logger = logging.getLogger(__name__)
 
class WebsiteMEServicesContactFOrm(http.Controller):

    @http.route(['/meservices/contact'], type='http', auth="user", methods=['POST'], website=True)
    def contacted_form(self, redirect=None, **post):
        if post:

            # Partner
            partner_id = request.env['res.partner'].sudo().create({
                'name': post['contact_name'],
                'street': post['street'],
                'zip': post['zip'],
                'city': post['city'],
                'mobile': post['mobile'],
            })

            # Sale Order
            sale_order_id = request.env['sale.order'].sudo().create({
                'partner_id': partner_id.id,
            })

            # Product
            product_id = request.env['product.product'].sudo().search([('default_code', '=', 'intervention')])
            if product_id:
                
                # Sale Order Line
                line_description = _('Insect type: ') + post['insect_type']
                line_description += _('\nNest location: ') + post['nest_location']
                line_description += _('\nDetails: ') + post['details']
                if 'already_came' in post:
                    line_description += _('\nAlready came on: ') + post['already_came']
                else:
                    post['already_came'] = 'False'
                line_description += _('\nNotes: ') + post['description']

                sale_order_line_id = request.env['sale.order.line'].sudo().create({
                    'order_id': sale_order_id.id,
                    'product_id': product_id.id,
                    'insect_type': post['insect_type'],
                    'nest_location': post['nest_location'],
                    'situation_details': post['details'],
                    'already_came': post['already_came'],
                    
                    'notes': post['description'],
                    'name': line_description,
                })
                # 'already_came_date': post['already_came_date'],

            _logger.debug("\n\n Request: %s", request)
            #company = request.env['']

            email_desc = _("Hello,<br />A new request has been made on your website.")
            email_desc += _("<br />Nom: ") + post['contact_name']
            email_desc += _("<br />Info: ") + line_description.replace('\n', '<br />')
            email_desc += _("<br /><br />Have a great day")

            mail_id = request.env['mail.mail'].create({
                'body_html': email_desc,
                'subject': 'Website: New demand',
                'email_to': 'valentinthirion@gmail.com',
                'email_from': 'noreply@meservices.be',
                'state': 'outgoing',
                'type': 'email',
                'auto_delete': False,
            })
            request.env['mail.mail'].send([mail_id])
