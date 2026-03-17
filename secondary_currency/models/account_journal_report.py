from odoo import models, api

class AccountJournalReportHandler(models.AbstractModel):
    _name='account.journal.report.custom.handler'
    _inherit = 'account.journal.report.handler'


    def _report_custom_engine_journal_report(self, expressions, options, date_scope, current_groupby, next_groupby, offset=0, limit=None, warnings=None):
        res = super()._report_custom_engine_journal_report(
            expressions, options, date_scope, current_groupby, next_groupby, 
            offset, limit, warnings
        )
        
        new_res = []
        for line_id, line_vals in res:
            real_id = int(line_id.split(',')[1]) if isinstance(line_id, str) else line_id
                
            move_line = self.env['account.move.line'].browse(real_id)
            
            new_vals = line_vals.copy()
            new_vals.update({
                'debit2': move_line.debit2, 
                'credit2': move_line.credit2,
                'balance2': move_line.balance2, 
            })
            new_res.append((line_id, new_vals))
            
        return new_res

    def _generate_document_data_for_export(self, report, options, export_type='pdf'):
        data = super()._generate_document_data_for_export(report, options, export_type=export_type)

        for journal in data.get('journals_vals', []):
            for line in journal.get('lines', []):
                move_line = self.env['account.move.line'].browse(line['id'])
                line.update({
                    'debit2': move_line.debit2,
                    'credit2': move_line.credit2,
                    'balance2': move_line.balance2,
                })
        
        return data