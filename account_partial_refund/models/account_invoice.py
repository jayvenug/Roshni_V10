# -*- coding: utf-8 -*-

from odoo import models, api, fields

MAGIC_COLUMNS = ('id', 'create_uid', 'create_date', 'write_uid', 'write_date')


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _refund_cleanup_lines(self, lines):
        result = []
        refunded_products = []
        if self._context.get('refund_line_ids', False):
            invoice_refunds = self.env['invoice.refund.line'].browse(
                [refund_line[1] for refund_line in
                 self._context.get('refund_line_ids', False)])
            refunded_products = reduce(lambda a, b: dict(
                a, **b), [{invoice_refund.invoice_line_id.id:
                           invoice_refund.refund_qty}
                          for invoice_refund in invoice_refunds])
            for line in lines:
                values = {}
                for name, field in line._fields.iteritems():
                    if name in MAGIC_COLUMNS:
                        continue
                    elif field.type == 'many2one':
                        values[name] = line[name].id
                    elif field.type not in ['many2many', 'one2many']:
                        values[name] = line[name]
                    elif name == 'invoice_line_tax_ids':
                        values[name] = [(6, 0, line[name].ids)]
                if line._name == 'account.invoice.line' and \
                        line.id in refunded_products:
                    values['quantity'] = refunded_products[line.id]
                    result.append((0, 0, values))

                    # Calculate Remaining Quantities which can be
                    # refunded next time.
                    line.refund_qty = line.refund_qty + \
                        refunded_products[line.id]
            return result
        return super(AccountInvoice, self)._refund_cleanup_lines(lines)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    refund_qty = fields.Float('Refunded Qty', default=0.0)
    to_refund_qty = fields.Float(
        'To Refund Qty', compute='compute_to_reund_qty')

    @api.multi
    @api.depends('quantity', 'refund_qty')
    def compute_to_reund_qty(self):
        for line in self:
            # Set Quantity which can be refunded.
            line.to_refund_qty = line.quantity - line.refund_qty
