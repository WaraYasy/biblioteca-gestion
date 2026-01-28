# -*- coding: utf-8 -*-
"""
Módulo de libros para la gestión de biblioteca en Odoo.
Define el modelo Libro que gestiona la información de los libros,
su valoración calculada automáticamente y sus relaciones con autores y categorías.

Autores: Arantxa, Wara
"""

from odoo import models, fields, api


class Libro(models.Model):
    """
    Modelo para gestionar los libros de la biblioteca.
    Permite registrar información detallada de cada libro incluyendo
    su valoración calculada automáticamente.
    
    Attributes:
        _name (str): Identificador del modelo (libro.libro)
        _description (str): Descripción del modelo
        _rec_name (str): Campo usado para mostrar y buscar el libro
    """
    _name = 'libro.libro'
    _description = 'Libro de la biblioteca'
    _rec_name = 'titulo'  # Campo usado para mostrar y buscar el libro

    # --- Campos básicos del libro ---
    titulo = fields.Char(
        string='Título del libro',
        required=True,
        help='Título completo del libro'
    )

    isbn = fields.Char(
        string='ISBN (13 dígitos)',
        required=True,
        size=13,
        help='Código ISBN de 13 dígitos'
    )

    fecha_publicacion = fields.Date(
        string='Fecha de publicación',
        required=True,
        help='Fecha en que se publicó el libro'
    )

    editorial = fields.Char(
        string='Editorial',
        help='Nombre de la editorial'
    )

    # --- Género literario con opciones predefinidas ---
    genero = fields.Selection(
        selection=[
            ('novela', 'Novela'),
            ('poesia', 'Poesía'),
            ('ensayo', 'Ensayo'),
            ('teatro', 'Teatro'),
            ('ciencia_ficcion', 'Ciencia Ficción'),
            ('fantasia', 'Fantasía'),
            ('terror', 'Terror'),
            ('romance', 'Romance'),
            ('historia', 'Historia'),
            ('biografia', 'Biografía'),
            ('infantil', 'Infantil'),
            ('juvenil', 'Juvenil'),
            ('otro', 'Otro'),
        ],
        string='Género literario',
        default='novela',
        help='Género literario del libro'
    )

    paginas = fields.Integer(
        string='Número de páginas',
        help='Cantidad total de páginas del libro'
    )

    disponible = fields.Boolean(
        string='Disponible para préstamo',
        default=True,
        help='Indica si el libro está disponible para préstamo'
    )

    sinopsis = fields.Text(
        string='Resumen del libro',
        help='Resumen o descripción del contenido del libro'
    )

    # --- Campos de valoración ---
    valoracion = fields.Float(
        string='Puntuación (0-10)',
        default=5.0,
        help='Puntuación del libro en escala de 0 a 10'
    )

    nivel_valoracion = fields.Char(
        string='Nivel de valoración (calculado)',
        compute='_compute_nivel_valoracion',
        store=True,
        help='Nivel calculado automáticamente según la valoración'
    )

    # --- Relación con autor ---
    autor_id = fields.Many2one(
        comodel_name='libro.autor',
        string='Autor',
        ondelete='set null',
        help='Autor del libro'
    )

    # --- Relación con categoría de la biblioteca ---
    categoria_id = fields.Many2one(
        comodel_name='libro.categoria',
        string='Categoría',
        ondelete='set null',
        help='Categoría del libro (ej: Novedades, Clásicos, Infantil)'
    )

    # --- Restricción SQL para validar ISBN único ---
    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'El ISBN debe ser único para cada libro.'),
    ]
    @api.depends('valoracion')
    def _compute_nivel_valoracion(self):
        """
        Calcula automáticamente el nivel de valoración según la puntuación.
        Este método se ejecuta cada vez que cambia el campo 'valoracion'.

        Rangos de valoración (con margen de +0.5):
        - 0 a 4.9: Baja
        - 5 a 6.9: Regular
        - 7 a 8.4: Buena
        - 8.5 a 9.4: Muy buena
        - 9.5 a 10: Excelente

        Returns:
            None: Asigna el valor calculado al campo 'nivel_valoracion' directamente
        """
        for libro in self:
            # Obtener la valoración, o 0 si está vacía
            valoracion = libro.valoracion or 0

            # Clasificar según rangos predefinidos
            if valoracion < 5:
                libro.nivel_valoracion = 'Baja'
            elif valoracion < 7:
                libro.nivel_valoracion = 'Regular'
            elif valoracion < 8.5:
                libro.nivel_valoracion = 'Buena'
            elif valoracion < 9.5:
                libro.nivel_valoracion = 'Muy buena'
            else:
                libro.nivel_valoracion = 'Excelente'

    # --- Restricción SQL para validar ISBN único ---
    _sql_constraints = [
        ('isbn_unique', 'UNIQUE(isbn)', 'El ISBN debe ser único para cada libro.'),
    ]
