from odoo import api, models, fields, _
import logging
_logger = logging.getLogger(__name__)

class AccountAsset(models.Model):
    _inherit = 'account.asset'

    company_currency2_id = fields.Many2one(
        related="company_id.currency2_id", 
        string='Secondary Company Currency',
        readonly=True, 
        store=True,
    )

    original_value2 = fields.Monetary(
        currency_field='company_currency2_id',
        store=True,
        readonly=False
    )

    salvage_value2 = fields.Monetary(
        currency_field='company_currency2_id',
        store=True,

    )

    book_value2 = fields.Monetary(
        compute='_compute_sec_values',
        currency_field='company_currency2_id',
        store=True,
    )

    depreciated_amount2 = fields.Monetary(
        currency_field='company_currency2_id',
        store=True,

    )


    @api.onchange('original_value', 'salvage_value','book_value', 'already_depreciated_amount_import')
    def _onchange_asset_values(self):
        for asset in self:
            rate_date = asset.acquisition_date or fields.Date.today() 
            depreciated_input = asset.already_depreciated_amount_import
            
            if asset.company_currency2_id and asset.company_id.currency_id:
                company = asset.company_id
                rate_date = asset.acquisition_date or fields.Date.today()
                
                asset.original_value2 = company.currency_id._convert(
                    asset.original_value, asset.company_currency2_id, company, rate_date
                )
                
                asset.salvage_value2 = company.currency_id._convert(
                    asset.salvage_value, asset.company_currency2_id, company, rate_date
                )
                asset.depreciated_amount2 = company.currency_id._convert(
                    depreciated_input, asset.company_currency2_id, company, rate_date
                )
                asset.book_value2 = (asset.original_value2 or 0.0) - (asset.depreciated_amount2 or 0.0)
                            
    @api.depends('original_value2', 'salvage_value2', 'depreciated_amount2')
    def _compute_sec_values(self):
        for asset in self:
            asset.book_value2 = asset.original_value2 - asset.depreciated_amount2       

    def _recompute_board(self, start_depreciation_date=False):
        move_vals = super()._recompute_board(start_depreciation_date)
        for asset in self:
            if asset.method_number > 0 and asset.company_currency2_id:
                periodic_amount2 = (asset.original_value2 - asset.salvage_value2) / asset.method_number
                    for line in move.line_ids:
                        depreciation_move_values.append(self.env['account.move']._prepare_move_for_asset_depreciation({
                        'amount2': periodic_amount2,                        
                    }))

        return move_vals

            

