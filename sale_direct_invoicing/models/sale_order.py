# -*- coding: utf-8 -*-
# © 2017 Jérome Guerriat
# © 2017 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        val = super(SaleOrder, self).action_confirm()
        invoices_ids = self.action_invoice_create()
        invoices = self.env['account.invoice'].browse(invoices_ids)
        invoices.action_invoice_open()
        return val
