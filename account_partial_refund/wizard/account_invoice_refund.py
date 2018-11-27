# -*- coding: utf-8 -*-

from odoo import models, api, fields
from odoo.exceptions import ValidationError


class InvoiceRefundLine(models.TransientModel):
    _name = "invoice.refund.line"

    invoice_line_id = fields.Many2one('account.invoice.line', 'Invoice Line')
    invoice_refund_id = fields.Many2one(
        'account.invoice.refund', 'Invoice Refund')
    product_id = fields.Many2one('product.product', 'Product')
    name = fields.Text('Description', required=True)
    invoiced_qty = fields.Float('Invoiced Qty')
    refund_qty = fields.Float('Refunded Qty')

    @api.constrains('refund_qty')
    def check_invoice_refund_qty(self):
        if self.refund_qty > self.invoiced_qty:
            raise ValidationError(
                "Refunded Quantity should be less than Invoice Quantity")


class AccountInvoiceRefund(models.TransientModel):
    """Refunds invoice"""

    _inherit = "account.invoice.refund"
    _description = "Invoice Refund"

    refund_line_ids = fields.One2many(
        'invoice.refund.line', 'invoice_refund_id', 'Refund lines')

    @api.model
    def default_get(self, default_fields):
        res = super(AccountInvoiceRefund, self).default_get(default_fields)
        if self._context.get('active_id', False):
            invoice_id = self.env['account.invoice'].browse(
                self._context.get('active_id', False))
            refund_lines = []
            for line in invoice_id.invoice_line_ids:
                if line.to_refund_qty > 0:
                    refund_lines.append((0, 0,
                                         {'invoice_line_id': line.id,
                                          'product_id': line.product_id and
                                          line.product_id.id,
                                          'name': line.name,
                                          'invoiced_qty': line.to_refund_qty,
                                          'refund_qty': line.to_refund_qty,
                                          }))
            line.compute_to_reund_qty()
            res['refund_line_ids'] = refund_lines
        return res
