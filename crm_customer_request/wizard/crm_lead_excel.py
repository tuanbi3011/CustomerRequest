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
            wb = openpyxl.load_workbook(filename=BytesIO(base64.b64decode(self.file)), read_only=True)
            ws = wb.active
            for record in ws.iter_rows(min_row=2, max_row=None, min_col=None, max_col=None, values_only=True):
                # search if the customer exist else create
                search = self.env['crm.lead'].search([
                    ('name', '=', record[1])])
                if not search:
                    self.env['crm.lead'].create({
                        'email': record[0],
                        'name': record[1],
                        'date_close': record[2],
                        'phone': record[3],
                        'private_note': record[4],
                        'customer_request': record[5]})
        except:
            raise UserError(_('Please insert a valid file'))

#    def action_import_customer(self):
#        return {
#            'name': 'Import Customer',
#            'type': 'ir.actions.act_window',
#            'res_model': 'crm.lead.form.excel.inherit',
#            'view_mode': 'form',
#            'view_type': 'form',
#            'target': 'new',
#        }

#    @property
#    def action_lost_reason_apply(self):
#        leads = self.env['crm.lead'].browse(self.env.context.get('active_ids'))
#        return leads.action_set_lost(lost_reason=self.file.id)
