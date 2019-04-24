# -*- coding: utf-8 -*-

import logging
from openerp import http, _
from openerp.http import request
from datetime import datetime

_logger = logging.getLogger(__name__)
 
class WebsiteMEServicesContactForm(http.Controller):

    @http.route(['/contactform'], type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def contacted_form(self, **post):
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
                already_came_date = ''
                if 'already_came' in post:
                    already_came_date = datetime.strptime(post['already_came_date'], '%Y-%m-%d')
                    line_description += _('\nAlready came on: ') + datetime.strftime(already_came_date, '%d/%m/%Y')
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
                    'already_came_date': already_came_date,
                    'notes': post['description'],
                    'name': line_description,
                })
                # 

            #company = request.env['']

            email_desc = _("Hello,<br />A new request has been made on your website.<br />")
            email_desc += _("<br /><b><u>Name:</b></u> ") + post['contact_name']
            email_desc += _("<br /><b><u>Mobile:</b></u> ") + post['mobile']
            email_desc += _("<br /><b><u>Address:</b></u> ") + post['street'] + ", " + post['zip'] + " " + post['city']
            email_desc += _("<br />")
            email_desc += _("<br /><b><u>Info:</b></u> <br />") + line_description.replace('\n', '<br />')
            email_desc += _("<br /><br />Have a great day")
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            url = "%s/web#id=%s&view_type=form&model=sale.order" % (base_url, sale_order_id.id)
            email_desc += _("<br />check it out here: <a href='") + url + "'>here</a>"

            mail_id = request.env['mail.mail'].sudo().create({
                'body_html': email_desc,
                'subject': 'Website: New demand',
                'email_to': 'valentinthirion@gmail.com',
                'email_from': 'noreply@meservices.be',
                'state': 'outgoing',
                'type': 'email',
                'auto_delete': False,
            })
            request.env['mail.mail'].sudo().send([mail_id])

            return request.render('meservices.contact_form_sent', {'result': 'OK'})
        else:
            return request.redirect("/")
