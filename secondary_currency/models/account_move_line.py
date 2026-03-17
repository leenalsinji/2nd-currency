from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from odoo.tools import SQL

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    company_currency2_id = fields.Many2one(
        related="company_id.currency2_id", 
        string='Secondary Company Currency',
        readonly=True, 
        store=True,
    )
    
    debit2 = fields.Monetary(
        string='Secondary Debit', 
        store=True, 
        currency_field='company_currency2_id',
        compute='_compute_secondary_amounts',
        readonly=False,
    )
    
    credit2 = fields.Monetary(
        string='Secondary Credit', 
        store=True, 
        currency_field='company_currency2_id',
        compute='_compute_secondary_amounts',
        readonly=False,
    )
    
    balance2 = fields.Monetary(
        string='Secondary Balance',
        compute='_compute_secondary_amounts',
        store=True,
        currency_field='company_currency2_id' 
    )
    
    amount2 = fields.Monetary(
        string='Secondary Amount',
        compute='_compute_secondary_amounts',
        store=True,
        readonly=False,
        currency_field='company_currency2_id',
    )

    @api.depends('debit', 'credit', 'date', 'company_currency2_id', 'move_id.asset_id')
    def _compute_secondary_amounts(self):
        for line in self:
            if line.move_id.asset_id:
                continue 
            if line.company_currency2_id and line.company_id.currency_id:
                rate_date = line.date or fields.Date.today()
                company = line.company_id 
                
                d2 = company.currency_id._convert(line.debit, line.company_currency2_id, company, rate_date)
                c2 = company.currency_id._convert(line.credit, line.company_currency2_id, company, rate_date)
                
                line.debit2 = d2
                line.credit2 = c2
                line.balance2 = d2 - c2
                line.amount2 = line.balance2
            else:
                line.debit2 = line.credit2 = line.amount2 = line.balance2 = 0.0

        
    @api.constrains('amount_currency', 'amount2') 
    def _check_amount2(self):
        for line in self:
            if line.amount2 and line.amount_currency:
                if (line.amount_currency * line.amount2) < 0:
                    raise ValidationError(_("The sign of Secondary Amount must match the sign of the original Amount."))