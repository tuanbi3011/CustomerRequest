# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CustomerRequest(models.Model):
    _name = 'crm.customer.request'
    _description = 'CRM Customer Request'

#   product_id = fields.Many2one('product.template', required=1, readonly=True)
    product_id = fields.Many2one('product.template', required=1)
    opportunity_id = fields.Many2one('crm.lead', required=1)
    date = fields.Date(required=1, default=fields.Date.today)
    qty = fields.Float(string='Quantity', default=1)
    description = fields.Char()
