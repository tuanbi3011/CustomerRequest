from odoo import fields, models, api
import openpyxl
import base64
from io import BytesIO
from odoo.exceptions import UserError

class CrmLeadExcel(models.TransientModel):
    _name = 'crm.lead.excel'

    file = fields.Binary(string="File", required=True)

    def import_customer(self, _=None):
        try:
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True )
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,max_col=None, values_only=True):
# search if the customer exist else create
                search = self.env['res.partner'].search([
                    ('name', '=', record[1]),
                    ('customer_rank', '=', True)])
                if not search:
                    self.env['res.partner'].create({
                            'ref': record[0],
                            'name': record[1],
                            'street': record[2],
                            'state_id': self.env['res.country.state'].search([
                                        ('name', '=', record[3])]).id,
                                        'country_id': self.env['res.country'].search([
                                                        ('code', '=', record[4])]).id,
                                                        'zip': record[5],
                                                        'phone': record[6],
                                                        'email': record[7],
                                                        'customer_rank': True})
        except:
            raise UserError(_('Please insert a valid file'))