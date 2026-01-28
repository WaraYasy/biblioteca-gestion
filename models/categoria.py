# -*- coding: utf-8 -*-
"""
Módulo de categorías para la gestión de biblioteca en Odoo.
Define el modelo Categoría que organiza los libros por secciones
y proporciona información sobre el número de libros en cada categoría.

Autores: Arantxa, Wara
"""

from odoo import models, fields, api


class Categoria(models.Model):
    """
    Modelo para gestionar las categorías de la biblioteca.
    Permite organizar los libros por categorías o secciones.
    
    Attributes:
        _name (str): Identificador del modelo (libro.categoria)
        _description (str): Descripción del modelo
    """
    _name = 'libro.categoria'
    _description = 'Categoría de la biblioteca'

    # --- Campos de la categoría ---
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la categoría (ej: Novedades, Clásicos, Infantil, Recomendados)'
    )

    descripcion = fields.Text(
        string='Descripción',
        help='Descripción de la categoría'
    )

    ubicacion = fields.Char(
        string='Ubicación',
        help='Ubicación física en la biblioteca (ej: Planta baja, Pasillo 3)'
    )

    color = fields.Integer(
        string='Color',
        default=0,
        help='Color para mostrar en las etiquetas'
    )

    # --- Relación inversa con libros ---
    # One2many: Una categoría puede tener muchos libros
    libro_ids = fields.One2many(
        comodel_name='libro.libro',
        inverse_name='categoria_id',
        string='Libros',
        help='Libros en esta categoría'
    )

    # --- Campo calculado: cantidad de libros ---
    # Computed field que se actualiza automáticamente
    cantidad_libros = fields.Integer(
        string='Cantidad de libros',
        compute='_compute_cantidad_libros',
        help='Número de libros en esta categoría'
    )

    def _compute_cantidad_libros(self):
        """
        Calcula la cantidad de libros en cada categoría.
        Se ejecuta automáticamente cuando cambia la relación 'libro_ids'.

        Returns:
            None: Asigna el valor calculado al campo 'cantidad_libros' directamente
        """
        for categoria in self:
            # Contar la cantidad de libros relacionados con esta categoría
            categoria.cantidad_libros = len(categoria.libro_ids)