# -*- coding: utf-8 -*-

from odoo import models, fields


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
        help='Estado actual del préstamo'
    )

    # --- Multa por retraso ---
    multa = fields.Float(
        string='Multa por retraso',
        help='Importe de la multa por retraso en la devolución'
    )
