from odoo import models, api, fields
from pprint import pprint

class AdjustmentLines(models.Model):
    _inherit = 'stock.valuation.adjustment.lines'

    def _create_account_move_line(self, move, credit_account_id, debit_account_id, qty_out, already_out_account_id):
        """
        inherit to add analytic account on landed cost STJ line
        """
        res = super(AdjustmentLines, self)._create_account_move_line(move, credit_account_id, debit_account_id, qty_out, already_out_account_id)
        #check if analytic account is need to be set
        start_date = self.move_id.picking_id.date_done
        end_date = self.create_date
        picking_to_check = self.env['stock.move'].search([('picking_id.date_done', '>=', start_date), ('picking_id.date_done', '<=',end_date),('product_id','=',self.product_id.id),('state','=','done')])
        picking_to_check = picking_to_check.filtered(lambda x: x._is_out())
        so = picking_to_check.mapped('sale_line_id').mapped('order_id')
        customer = so.mapped('partner_id')
        categ = customer.mapped('category_id')
        analytic_account = self.env['account.analytic.account'].search([('customer_tags_ids', 'in', categ.ids)])
        account_type = 'expense_direct_cost'
        account = self.env['account.account'].search([('account_type', '=', account_type)])
        if not categ:
            return res
        if len(categ) == 1:
            for entry in res:
                if entry[2]['account_id'] in account.ids:
                    analytic_account = self.env['account.analytic.account'].search([('customer_tags_ids', 'in', categ.ids)])
                    entry[2]['analytic_distribution'] = {
                                                            str(analytic_account.id): 100,
                                                        }
            return res
        elif len(categ) > 1:
            qty_dict = []
            for cat in categ:
                qty=0
                for move_line in picking_to_check:
                    if move_line.sale_line_id.order_id.x_studio_tags and move_line.sale_line_id.order_id.x_studio_tags[0] == cat:
                        qty+=move_line.product_uom_qty
                analytic_account = self.env['account.analytic.account'].search([('customer_tags_ids', 'in', [cat.id])])
                qty_dict.append({
                    'category':cat,
                    'analytic_account':analytic_account,
                    'qty':qty
                })
            sorted_qty_dic = sorted(qty_dict, key=lambda x: x['qty'])
            for entry in res:
                qty_out = 0
                if entry[2]['account_id'] in account.ids:
                    # Modify the entry as needed (Example: updating name)
                    text =  entry[2]['name']
                    # entry[2]['name'] += 'mmmmmm'
                    parts = text.split(":")
                    if len(parts) > 1:
                        number_part = parts[1].strip().split(" ")[0]  # Take the first part after ':'
                        result = float(number_part)
                        qty_out = result
                        initial_debit = entry[2]['debit']
                        entry[2]['analytic_distribution'] = {
                                                            str(sorted_qty_dic[0]['analytic_account'].id): 100,
                                                        }
                        entry[2]['debit'] = (entry[2]['debit']/qty_out) * sorted_qty_dic[0]['qty']
                                                        
                    res.append((0,0,{
                        'name': entry[2]['name'],
                        'account_id': entry[2]['account_id'],
                        'analytic_distribution': {str(sorted_qty_dic[1]['analytic_account'].id): 100},
                        'debit': initial_debit - entry[2]['debit'],
                    }))
                    break

        return res