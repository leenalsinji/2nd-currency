from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare
import logging
_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    company_currency2_id = fields.Many2one(
        related='company_id.currency2_id', 
        string="Secondary Currency", 
        readonly=True,
    )
    depreciation_value2 = fields.Monetary(
        compute='_compute_depreciation_value2',
        store=True,
        )
        
    @api.constrains('line_ids', 'line.debit2', 'line.credit2')
    def _check_secondary_balanced(self):
        for move in self:
            if not move.company_id.currency2_id:
                continue

            prec = move.company_id.currency2_id.decimal_places or 2
            
            total_debit2 = sum(line.debit2 for line in move.line_ids)
            total_credit2 = sum(line.credit2 for line in move.line_ids)

            if float_compare(total_debit2, total_credit2, precision_digits=prec) != 0:
                raise ValidationError(_(
                    "The Journal Entry is not balanced at the Secondary Currency!\n"))

    @api.constrains('date')
    def _check_date_not_changing_secondary(self):
        for move in self:
            if move.state == 'posted' and move.company_id.currency2_id:
                pass 

    @api.depends('line_ids.balance2')
    def _compute_depreciation_value2(self):
        for move in self:
            asset = move.asset_id or move.reversed_entry_id.asset_id  
            if asset and asset.company_currency2_id:
                depreciation_lines = move.line_ids.filtered(lambda l: l.account_id == asset.account_depreciation_id)
                asset_depreciation2 = sum(depreciation_lines.mapped('balance2'))
                if any(line.account_id == asset.account_asset_id for line in move.line_ids):
                     pass
                move.depreciation_value2 = asset_depreciation2
            else:
                move.depreciation_value2 = 0.0

                
    @api.model
    def _prepare_move_for_asset_depreciation(self, vals): 
       amount2 = 
      
        move_vals = super()._prepare_move_for_asset_depreciation(vals)      
        if amount2:
            for line in move_vals.get('line_ids', []):
                line_vals = line[2]

                if line_vals.get('debit', 0.0) > 0:
                    line_vals.update({'debit2': amount2, 'balance2': amount2})
                elif line_vals.get('credit', 0.0) > 0:
                    line_vals.update({'credit2': amount2, 'balance2': -amount2})

        return move_vals


        


