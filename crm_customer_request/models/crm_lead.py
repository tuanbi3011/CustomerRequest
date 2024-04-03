# -*- coding: utf-8 -*-
import requests

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    request_ids = fields.One2many('crm.customer.request', 'opportunity_id')
    total_sales = fields.Monetary(compute='_compute_total_sales', currency_field='company_currency',
                                  string='Total Sales', tracking=True, store=True)
    expected_revenue = fields.Monetary(compute='_compute_expected_revenue', currency_field='company_currency',
                                       string='Expected Revenue', tracking=True)
    opportunity_state = fields.Selection([
        ('new', 'New'),
        ('other', 'Other')
    ], string='Opportunity State', compute='_compute_opportunity_state', store=True)
    request_line_ids = fields.One2many('crm.customer.request', 'product_id')

    @api.depends('request_ids')
    def _compute_total_sales(self):
        for lead in self:
            lead.total_sales = sum(lead.request_ids.mapped('qty'))

    @api.depends('request_ids')
    def _compute_expected_revenue(self):
        for lead in self:
            total_sale = sum(request.qty * requests.product_id.list_price for request in lead.request_ids)
            lead.expected_revenue = total_sale

    @api.depends('request_ids')
    def _compute_opportunity_state(self):
        for lead in self:
            if lead.state_id and lead.state_id.name == 'New':
                lead.opportunity_state = 'new'
            else:
                lead.opportunity_state = 'other'

#    @api.constrains('opportunity_state')
#    def _check_opportunity_state(self):
#        for lead in self:
#            if lead.opportunity_state == 'new':
#                continue
#            else:
#                raise ValidationError("Can not modify record")

    @api.model
    def create_quotation_from_opportunity(self, opportunity_id):
        opportunity = self.env['crm.lead'].browse(opportunity_id)
        sale_order_vals = {
            'partner_id': opportunity.partner_id.id,
            'opportunity_id': opportunity.id,
        }
        sale_order = self.env['sale.order'].create(sale_order_vals)

        for request in opportunity.request_ids:
            order_line_vals = {
                'order_id': sale_order.id,
                'product_id': request.product_id.id,
                'product_uom_qty': request.qty,
            }
            self.env['sale.order.line'].create(order_line_vals)

        return {
            'name': ('Quotation Created'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
        }

    @api.model
    def action_import_customer(self):
        return {
            'name': 'Import Customer',
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead.form.excel.inherit',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }
