# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Prestamo(models.Model):
    """
    Modelo para gestionar los préstamos de libros.
    Registra qué libro fue prestado, a quién y el estado del préstamo.
    """
    _name = 'libro.prestamo'
    _description = 'Préstamo de libro'

    # --- Relación con el libro prestado ---
    libro_id = fields.Many2one(
        comodel_name='libro.libro',
        string='Libro prestado',
        required=True,
        ondelete='restrict',
        help='Libro que se presta'
    )

    # --- Relación con el usuario que solicita el préstamo ---
    # Usamos res.partner como modelo de usuario (contactos de Odoo)
    usuario_id = fields.Many2one(
        comodel_name='res.partner',
        string='Usuario que pide',
        required=True,
        ondelete='restrict',
        help='Usuario que solicita el préstamo'
    )

    # --- Fechas del préstamo ---
    fecha_prestamo = fields.Date(
        string='Fecha de préstamo',
        required=True,
        default=fields.Date.today,
        help='Fecha en que se realizó el préstamo'
    )

    fecha_devolucion = fields.Date(
        string='Fecha de devolución',
        help='Fecha en que se devolvió el libro'
    )

    # --- Estado del préstamo ---
    estado = fields.Selection(
        selection=[
            ('prestado', 'Prestado'),
            ('devuelto', 'Devuelto'),
            ('retrasado', 'Retrasado'),
            ('perdido', 'Perdido'),
        ],
        string='Estado del préstamo',
        default='prestado',
        required=True,
        help='Estado actual del préstamo'
    )

    # --- Multa por retraso ---
    multa = fields.Float(
        string='Multa por retraso',
        help='Importe de la multa por retraso en la devolución'
    )

    # Validación: Fecha de devolución debe ser posterior a fecha de préstamo
    @api.constrains('fecha_prestamo', 'fecha_devolucion')
    def _check_fechas(self):
        for prestamo in self:
            if prestamo.fecha_devolucion and prestamo.fecha_prestamo:
                if prestamo.fecha_devolucion < prestamo.fecha_prestamo:
                    raise ValidationError(
                        'La fecha de devolución debe ser posterior a la fecha de préstamo.\n'
                        f'Fecha de préstamo: {prestamo.fecha_prestamo}\n'
                        f'Fecha de devolución: {prestamo.fecha_devolucion}'
                    )

    # Validación: No permitir prestar un libro que ya está prestado
    @api.constrains('libro_id', 'estado')
    def _check_libro_ya_prestado(self):
        for prestamo in self:
            # Solo validar si el estado es prestado o retrasado (activos)
            if prestamo.estado in ['prestado', 'retrasado']:
                # Buscar si hay otro préstamo activo del mismo libro
                otros_prestamos = self.search([
                    ('libro_id', '=', prestamo.libro_id.id),
                    ('estado', 'in', ['prestado', 'retrasado']),
                    ('id', '!=', prestamo.id)
                ])

                if otros_prestamos:
                    raise ValidationError(
                        f'El libro "{prestamo.libro_id.titulo}" ya está prestado. '
                        'Debe devolverse antes de crear un nuevo préstamo.'
                    )

    # Al crear un préstamo, marcar el libro como no disponible
    @api.model_create_multi
    def create(self, vals_list):
        prestamos = super().create(vals_list)
        for prestamo in prestamos:
            if prestamo.estado in ['prestado', 'retrasado']:
                prestamo.libro_id.disponible = False
        return prestamos

    # Al modificar el estado, actualizar disponibilidad del libro
    def write(self, vals):
        result = super().write(vals)
        if 'estado' in vals:
            for prestamo in self:
                if prestamo.estado == 'devuelto':
                    # Marcar libro como disponible
                    prestamo.libro_id.disponible = True
                elif prestamo.estado in ['prestado', 'retrasado']:
                    # Marcar libro como no disponible
                    prestamo.libro_id.disponible = False
        return result
