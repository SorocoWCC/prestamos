# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import ValidationError
from odoo.exceptions import UserError
from openerp.exceptions import Warning
from openerp import models, fields, api
from datetime import datetime
from pytz import timezone 
from datetime import timedelta 

class abono(models.Model):

    @api.model
    def _get_name(self):
        return str(self.env['res.users'].browse(self.env.uid).name)

    @api.model
    def _get_date(self):
        return str(fields.Date.today())

    _name = "abono"
    _description = "Abono Prestamo"
    _inherit = 'mail.thread'

    prestamo_id = fields.Many2one(comodel_name='prestamo',string='Prestamo')
    responsable = fields.Char(size=50, string="Responsable", default=_get_name,  readonly=True)
    detalle = fields.Char(size=50, string="Detalle")
    fecha = fields.Date(string='Fecha', default=_get_date, readonly=True)
    monto = fields.Float(string='Monto', required=True)
    saldo = fields.Float(string='Saldo')
    state = fields.Selection([('borrador','Borrador'), ('cerrado','Cerrado')], string='state', default="borrador")

    @api.one
    @api.constrains('monto')
    def _check_monto(self): 
        if self.monto == 0:
            raise Warning ("Error: Ingrese el monto del Abono.")
        if self.monto > self.prestamo_id.saldo:
            raise Warning ("Error: El monto del abono es mayor que el saldo del prestamo.")

        if self.prestamo_id.saldo == self.monto:
            self.prestamo_id.state = "cerrado"
            self.prestamo_id.saldo = 0
        else:
            self.saldo  = self .prestamo_id.saldo - self.monto        
       
        # Estado del abono
        self.state = 'cerrado'

    @api.multi
    def action_imprimir(self):
        return self.env.ref('prestamos.custom_report_abono').report_action(self)


