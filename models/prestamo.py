# -*- coding: utf-8 -*-
"""
Módulo de préstamos para la gestión de biblioteca en Odoo.
Define el modelo Préstamo que gestiona los préstamos de libros,
validaciones de fechas y control de disponibilidad de libros.

Autores: Arantxa, Wara
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Prestamo(models.Model):
    """
    Modelo para gestionar los préstamos de libros.
    Registra qué libro fue prestado, a quién y el estado del préstamo.
    Incluye validaciones para garantizar integridad de datos.
    
    Attributes:
        _name (str): Identificador del modelo (libro.prestamo)
        _description (str): Descripción del modelo
    """
    _name = 'libro.prestamo'
    _description = 'Préstamo de libro'

    # --- Relación con el libro prestado ---
    # Many2one: Muchos préstamos pueden referirse al mismo libro
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
    # Selection: Campo con valores predefinidos
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
        """
        Valida que la fecha de devolución sea posterior a la fecha de préstamo.
        Se ejecuta automáticamente cuando se modifican estos campos.

        Raises:
            ValidationError: Si la fecha de devolución es anterior a la fecha de préstamo
        """
        for prestamo in self:
            # Solo validar si ambas fechas están definidas
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
        """
        Valida que no haya múltiples préstamos activos del mismo libro.
        Impide que se preste un libro si ya hay otro préstamo activo.

        Raises:
            ValidationError: Si el libro ya tiene un préstamo activo
        """
        for prestamo in self:
            # Solo validar si el estado es prestado o retrasado (préstamos activos)
            if prestamo.estado in ['prestado', 'retrasado']:
                # Buscar si hay otro préstamo activo del mismo libro (excluyendo este)
                otros_prestamos = self.search([
                    ('libro_id', '=', prestamo.libro_id.id),
                    ('estado', 'in', ['prestado', 'retrasado']),
                    ('id', '!=', prestamo.id)  # Excluir el préstamo actual
                ])

                # Si hay otros préstamos activos, lanzar error
                if otros_prestamos:
                    raise ValidationError(
                        f'El libro "{prestamo.libro_id.titulo}" ya está prestado. '
                        'Debe devolverse antes de crear un nuevo préstamo.'
                    )

    # Al crear un préstamo, marcar el libro como no disponible
    @api.model_create_multi
    def create(self, vals_list):
        """
        Crea nuevos registros de préstamo y actualiza la disponibilidad del libro.
        Cuando se crea un préstamo con estado 'prestado' o 'retrasado',
        el libro se marca como no disponible automáticamente.

        Args:
            vals_list: Lista de diccionarios con los valores para crear los préstamos

        Returns:
            prestamos: Registros de préstamo creados
        """
        prestamos = super().create(vals_list)
        # Para cada préstamo creado, actualizar la disponibilidad del libro
        for prestamo in prestamos:
            if prestamo.estado in ['prestado', 'retrasado']:
                # Marcar el libro como no disponible
                prestamo.libro_id.disponible = False
        return prestamos

    # Al modificar el estado, actualizar disponibilidad del libro
    def write(self, vals):
        """
        Actualiza los registros de préstamo y sincroniza la disponibilidad del libro.
        Cuando cambia el estado del préstamo, se actualiza automáticamente
        el estado de disponibilidad del libro asociado.

        Args:
            vals: Diccionario con los campos a actualizar

        Returns:
            result: Resultado de la operación de actualización
        """
        result = super().write(vals)
        # Si se modifica el estado del préstamo, actualizar disponibilidad del libro
        if 'estado' in vals:
            for prestamo in self:
                if prestamo.estado == 'devuelto':
                    # Marcar libro como disponible si fue devuelto
                    prestamo.libro_id.disponible = True
                elif prestamo.estado in ['prestado', 'retrasado']:
                    # Marcar libro como no disponible si está en préstamo
                    prestamo.libro_id.disponible = False
        return result
