# -*- coding: utf-8 -*-

from odoo import models, fields


class Categoria(models.Model):
    """
    Modelo para gestionar las categorías de libros.
    Permite organizar los libros por temáticas con colores visuales.
    """
    _name = 'libro.categoria'
    _description = 'Categoría de libros'

    # --- Campos de la categoría ---
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la categoría (ej: Ciencias, Historia, Literatura)'
    )

    descripcion = fields.Text(
        string='Descripción',
        help='Descripción de la categoría'
    )

    color = fields.Integer(
        string='Color',
        default=0,
        help='Color para mostrar en las etiquetas'
    )

    # --- Relación inversa con libros ---
    libro_ids = fields.One2many(
        comodel_name='libro.libro',
        inverse_name='categoria_id',
        string='Libros',
        help='Libros en esta categoría'
    )

    # --- Campo calculado: cantidad de libros ---
    cantidad_libros = fields.Integer(
        string='Cantidad de libros',
        compute='_compute_cantidad_libros',
        help='Número de libros en esta categoría'
    )

    def _compute_cantidad_libros(self):
        for categoria in self:
            categoria.cantidad_libros = len(categoria.libro_ids)