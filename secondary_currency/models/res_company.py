from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ResCompany(models.Model):
    _inherit = 'res.company'

    currency2_id = fields.Many2one(
        'res.currency',
        string='Secondary Currency',
    )

    @api.onchange('currency2_id', 'currency_id')
    def _onchange_currency2_id(self):
        if self.currency2_id and self.currency_id:
            if self.currency2_id == self.currency_id:
                curr_name = self.currency2_id.name
                self.currency2_id = False                
                return {
                    'warning': {
                        'message': _("The Secondary Currency cannot be the same as the  Company Currency. Please choose a different one.")
                    }
                }