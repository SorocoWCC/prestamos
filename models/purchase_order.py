# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from odoo.exceptions import UserError
from openerp.exceptions import Warning
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone 
from datetime import timedelta  
import subprocess
import time
import base64

class purchase_order(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    prestamo_info = fields.Float(compute='_action_prestamo_info', store=True, default=0, string="Prestamo" )
    agregar_linea_prestamo = fields.Boolean(default=False)

    # Marcar la factura como pagada y la asocia con los cierres de caja
    @api.multi
    def action_quotation_paid(self):
        print("===========PRESTAMOS==============")

    # Agregar linea de prestamo en la orden de compra
    @api.one
    def action_take_picture(self):
        super().action_take_picture()
        print("===========PICTURE==============")
        print(self.prestamo_info)
        if self.prestamo_info > 0 and self.agregar_linea_prestamo == False:
            prestamo= self.env['prestamo'].search([['tipo', '=', 'cliente'], ['state', '=', 'abierto'], ['cliente_id.id', '=', self.partner_id.id]])

            if prestamo :
                res= self.env['product.template'].search([['name', '=', 'Prestamo'], ['default_code', '=', 'PR']])
                monto_abono = 0
                if res.list_price > prestamo[0].saldo :
                    monto_abono = prestamo[0].saldo
                else:
                    monto_abono = res.list_price

                self.order_line.create({'product_id': str(res.id), 'price_unit':str(monto_abono), 'order_id' : self.id, 'name': '[PR] Prestamo','calcular': True, 'date_planned': str(fields.Date.today()), 'product_qty': 1, 'product_uom': str(res.uom_po_id.id)})
                self.agregar_linea_prestamo = True

    @api.depends('partner_id')
    def _action_prestamo_info(self):
        print("Action Prestamo")
        prestamo= self.env['prestamo'].search([['tipo', '=', 'cliente'], ['state', '=', 'abierto'], ['cliente_id.id', '=', self.partner_id.id]])
        if prestamo :
            print("Hay prestamos")
            self.prestamo_info = prestamo[0].saldo
            print(self.prestamo_info)
