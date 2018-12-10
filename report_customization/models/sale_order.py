# -*- coding: utf-8 -*-
##############################################################################
#
# Part of Caret IT Solutions Pvt. Ltd. (Website: www.caretit.com).
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import api, fields, models, _


class  SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_loading_sheet(self):
        return self.env['report']\
        .get_action(self, 'report_customization.report_loadingsheet')


class  ProductUom(models.Model):
    _inherit = 'product.uom'

    general_name = fields.Char('UOM')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    vehicle_number = fields.Char('Vehicle Number')
    dispatch_reg_num = fields.Char('Dispatch Reg. No.')
    custom_entry_number = fields.Char('Custom Entry Number')

    @api.multi
    def custom_invoice_print(self):
        self.ensure_one()
        self.sent = True
        return self.env['report']\
        .get_action(self, 'report_customization.report_invoice_custom')

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_flag = fields.Selection([('import', 'IMPORT'), ('local', 'LOCAL')], string='Customer Flag')

class AccountBatchDeposit(models.Model):
    _inherit = 'account.batch.deposit'

    pay_in_slip = fields.Char('Pay In Slip For')

    @api.multi
    def get_company_bank(self):
        user = self.env['res.users'].browse(self.env.uid)
        bank_id = self.env['res.partner.bank'].search([('partner_id', '=', user.partner_id.id)])
        return bank_id

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    branch = fields.Char('Branch')
    bank_acc_id = fields.Many2one('res.bank', string="Bank")
