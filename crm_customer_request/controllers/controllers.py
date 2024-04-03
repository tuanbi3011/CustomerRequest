# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class LeadAPI(http.Controller):

    @http.route('/api/create_lead', type='json', auth='none', methods=['POST'])
    def create_lead_api(self, **post):
        # Kiểm tra xem dữ liệu JSON có chứa các trường cần thiết không
        if not all(field in post for field in ['name', 'date_close', 'email', 'phone', 'private_note', 'request_ids']):
            return {'error': 'Missing required fields'}

        # Tạo lead mới với thông tin từ dữ liệu JSON
        lead_vals = {
            'partner_name': post.get('name'),
            'date_deadline': post.get('date_close'),
            'email_from': post.get('email'),
            'phone': post.get('phone'),
            'description': post.get('private_note'),
        }
        new_lead = request.env['crm.lead'].create(lead_vals)

        # Tạo yêu cầu của KH từ danh sách trong dữ liệu JSON
        for request_data in post.get('requests', []):
            product_id = request_data.get('product_id')
            quantity = request_data.get('quantity')
            request_date = request_data.get('date')

            # Tìm sản phẩm trong danh mục sản phẩm
            product = request.env['product.product'].search([('id', '=', product_id)], limit=1)

            # Nếu sản phẩm không tồn tại, bỏ qua
            if not product:
                continue
        request_vals = {
            'product_id': product.id,
            'product_uom_qty': quantity,
            'date_planned': request_date,
            'lead_id': new_lead.id,  # Liên kết yêu cầu với lead mới
        }
        request_obj = request.env['sale.order.line'].create(request_vals)

        return {'success': True, 'lead_id': new_lead.id}