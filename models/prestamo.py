# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from odoo.exceptions import UserError
from openerp.exceptions import Warning
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone 
from datetime import timedelta 

class prestamo(models.Model):
    _name = "prestamo"
    _description = "Prestamo"
    _inherit = 'mail.thread'

    empleado_id = fields.Many2one(comodel_name='hr.employee', string='Empleado')
    cliente_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    notas= fields.Text(string='Notas')
    fecha = fields.Date(string='Fecha', readonly=True)
    abono_ids = fields.One2many(comodel_name='abono',inverse_name='prestamo_id', string="Abonos")
    monto = fields.Float(string='Monto', required=True)
    total_abonos = fields.Float(compute='action_total_abonos', store=True, string="Total Abonos: ", readonly=True)
    saldo = fields.Float(compute='action_saldo', store=True, string="Saldo:", readonly=True)
    detalle = fields.Char(size=50, string="Detalle")
    fecha_abono = fields.Char(string="Fecha Abono", store=True)
    monto_abono = fields.Float(string="Monto Abono", store=True)
    refrescar_estado = fields.Float(compute='action_state', store=True, string="Saldo:")
    state = fields.Selection([('borrador','Borrador'), ('abierto','Abierto'), ('incobrable','Incobrable'), ('cerrado','Cerrado')], string='Estado', default="borrador")
    tipo = fields.Selection([('empleado','Empleado'), ('cliente','Cliente'), ('por_pagar','Por Pagar')], string='Tipo de Prestamo')

    @api.one
    @api.constrains('monto')
    def _check_monto(self): 
        if self.monto == 0:
            raise Warning ("Error: Ingrese el monto del prestamo.")
        else:
            self.state = "abierto"
            self.saldo = self.monto
            self.fecha = str(fields.Date.today())
            mensaje = "<p>Prestamo creado por : " + str(self.env.user.name) + " - " + datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d %H:%M:%S") + "</p>"
            self.message_post(body=mensaje, content_subtype='html')

    @api.one
    @api.constrains('cliente_id', 'empleado_id')
    def _check_cliente(self): 
        if self.tipo in ('cliente', 'por_pagar') and not self.cliente_id:
            raise Warning ("Error: Por favor seleccione el cliente.")
        if self.tipo == 'empleado' and not self.empleado_id:
            raise Warning ("Error: Por favor seleccione el empleado.")

    # Dinero de Abonos
    @api.one
    @api.depends('abono_ids')
    def action_total_abonos(self):  
        total=0
        for abono in self.abono_ids :
            total += abono.monto

        self.total_abonos = total

    # Calculo del Saldo
    @api.one
    @api.depends('total_abonos')
    def action_saldo(self): 
        if self.state == "abierto": 
                self.saldo  = self.monto - self.total_abonos

    # Marcar prestamo como cerrado
    @api.one
    def action_cerrado(self): 
        self.state = "cerrado"
        mensaje = "<p>Prestamo cerrado por : " + str(self.env.user.name) + " - " + datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d %H:%M:%S") + "</p>"
        self.message_post(body=mensaje, content_subtype='html')

    # Marcar prestamo como incobrable
    @api.one
    def action_incobrable(self): 
        self.state = "cerrado"
        mensaje = "<p>Prestamo incobrable por : " + str(self.env.user.name) + " - " + datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d %H:%M:%S") + "</p>"
        self.message_post(body=mensaje, content_subtype='html')

    # Marcar prestamo como incobrable
    @api.one
    def action_incobrable(self): 
        self.state = "cerrado"
        mensaje = "<p>Prestamo incobrable por : " + str(self.env.user.name) + " - " + datetime.now(timezone('America/Costa_Rica')).strftime("%Y-%m-%d %H:%M:%S") + "</p>"
        self.message_post(body=mensaje, content_subtype='html')
