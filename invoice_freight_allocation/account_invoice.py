# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv
from openerp.tools.translate import _


class account_invoice(osv.osv):

    _inherit = 'account.invoice'
    _columns = {
        'freight_alloc_ids': fields.one2many('account.invoice.freight.alloc', 'invoice_id', 'Freight Lines'),
    }

    def write(self, cr, uid, ids, vals, context=None):
        res = super(account_invoice, self).write(cr, uid, ids, vals, context=context)
        for invoice in self.browse(cr, uid, ids, context=context):
            if invoice.freight_alloc_ids:
                invoice_amount = invoice.amount_total - invoice.amount_tax
                freight_alloc = 0.0
                for alloc in invoice.freight_alloc_ids:
                    if alloc.invoice_id == invoice.id:
                        raise osv.except_osv(_('Error!'), _('You '))
                    freight_alloc += alloc.amount_alloc
                if freight_alloc != invoice_amount:
                    raise osv.except_osv(_('Error!'), _('Total Freight Allocation must equal Invoice Amount before Tax'))
        return res

account_invoice()


class account_invoice_freight_alloc(osv.osv):

    _name = 'account.invoice.freight.alloc'
    _description = 'Invoice Freight Allocation'

    _columns = {
        'invoice_id': fields.many2one('account.invoice', 'Invoice', ondelete="cascade"),
        'supplier_invoice_id': fields.many2one('account.invoice', 'Supplier Invoice', domain="[('type', '=', 'in_invoice'), ('id', '!=', parent.id)]", ondelete="restrict", required=True, help="Supplier Invoice, in which this invoice is paying for its freight"),
        'amount_alloc': fields.float('Allocation', required=True, digits_compute=dp.get_precision('Account')),
    }

account_invoice_freight_alloc()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
