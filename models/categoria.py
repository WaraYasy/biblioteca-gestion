# -*- coding: utf-8 -*-

from odoo import models, fields


class Categoria(models.Model):
    """
    Modelo para gestionar las zonas/secciones de la biblioteca.
    Permite organizar los libros por ubicación o sección especial.
    """
    _name = 'libro.categoria'
    _description = 'Zona de la biblioteca'

    # --- Campos de la categoría ---
    name = fields.Char(
        string='Nombre',
        required=True,
        help='Nombre de la zona (ej: Novedades, Clásicos, Infantil, Recomendados)'
    )

    descripcion = fields.Text(
        string='Descripción',
        help='Descripción de la zona'
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
    libro_ids = fields.One2many(
        comodel_name='libro.libro',
        inverse_name='categoria_id',
        string='Libros',
        help='Libros en esta zona'
    )

    # --- Campo calculado: cantidad de libros ---
    cantidad_libros = fields.Integer(
        string='Cantidad de libros',
        compute='_compute_cantidad_libros',
        help='Número de libros en esta zona'
    )

    def _compute_cantidad_libros(self):
        for categoria in self:
            categoria.cantidad_libros = len(categoria.libro_ids)