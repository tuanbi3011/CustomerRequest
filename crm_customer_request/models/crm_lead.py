# -*- coding: utf-8 -*-    
from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    request_ids = fields.One2many('crm.customer.request', 'opportunity_id') 
    total_sales = fields.Monetary(compute='_compute_total_sales', currency_field='company_currency', string='Total Sales', store=True)
    expected_revenue = fields.Monetary(compute='_compute_expected_revenue', currency_field='company_currency', string='Expected Revenue', tracking=True)
    opportunity_state = fields.Selection([
        ('new', 'New'),
        ('other', 'Other')
    ], string='Opportunity State', compute='_compute_opportunity_state', store=True)

    @api.depends('request_ids')
    def _compute_total_sales(self):
        for lead in self:
            lead.total_sales = sum(request.qty for request in lead.request_ids)
    
    @api.depends('request_ids')
    def _compute_expected_revenue(self):
        for lead in self:
            expected_revenue = sum(request.product_id.list_price * request.qty for request in lead.request_ids)
            lead.expected_revenue = expected_revenue

    @api.depends('request_ids')
    def _compute_opportunity_state(self):
        for lead in self:
            if lead.state == 'new':
                lead.opportunity_state = 'new'
            else:
                lead.opportunity_state = 'other'