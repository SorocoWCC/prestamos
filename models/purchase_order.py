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

    prestamo_saldo = fields.Float(compute='_action_prestamo_saldo', store=True, default=0, string="Prestamo" )
    prestamo_total = fields.Float(compute='_action_prestamo_saldo', store=True, string="Monto Prestamo" )
    agregar_linea_prestamo = fields.Boolean(default=False)

    
    @api.multi
    def button_confirm(self):
        super(purchase_order, self).button_confirm()
        if self.prestamo_saldo > 0 :
            prestamo= self.env['prestamo'].search([['tipo', '=', 'cliente'], ['state', '=', 'abierto'], ['cliente_id.id', '=', self.partner_id.id]])
            for line in self.order_line:
                if line.product_id.name == "Prestamo" and line.price_unit > 0:
                    # Valida que el monto del abono sea negativo para no pagar de mas al cliente
                        raise Warning ("Error: El monto del abono al prestamo debe de ser negativo")

    # Agregar linea de prestamo en la orden de compra
    @api.one
    def action_take_picture(self):
        super().action_take_picture()
        if self.prestamo_saldo > 0 and self.agregar_linea_prestamo == False:
            prestamo= self.env['prestamo'].search([['tipo', '=', 'cliente'], ['state', '=', 'abierto'], ['cliente_id.id', '=', self.partner_id.id]])

            if prestamo and self.agregar_linea_prestamo == False:
                res= self.env['product.template'].search([['name', '=', 'Prestamo'], ['default_code', '=', 'PR']])
                monto_abono = 0

                if abs(res.list_price) > prestamo[0].saldo :
                    monto_abono = prestamo[0].saldo
                else:
                    monto_abono = res.list_price

                self.order_line.create({'product_id': str(res.id), 'price_unit':str(-abs(monto_abono)), 'order_id' : self.id, 'name': '[PR] Prestamo','calcular': False, 'date_planned': str(fields.Date.today()), 'product_qty': 1, 'product_uom': str(res.uom_po_id.id)})
                self.agregar_linea_prestamo = True

    # Consultar si el proveedor tiene prestamo  
    @api.one          
    @api.depends('partner_id')
    def _action_prestamo_saldo(self):
        prestamo= self.env['prestamo'].search([['tipo', '=', 'cliente'], ['state', '=', 'abierto'], ['cliente_id.id', '=', self.partner_id.id]])
        if prestamo :
            self.prestamo_saldo = prestamo[0].saldo
            self.prestamo_total = prestamo[0].monto
