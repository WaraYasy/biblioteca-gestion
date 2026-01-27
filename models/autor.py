# -*- coding: utf-8 -*-
"""
Módulo de autores para la gestión de biblioteca en Odoo.
Define el modelo Autor que gestiona la información de los autores
y su relación con los libros.
"""

from odoo import models, fields


class Autor(models.Model):
    """
    Modelo para gestionar los autores de la biblioteca.
    Almacena información personal del autor y la lista de sus libros.
    
    Attributes:
        _name (str): Identificador del modelo (libro.autor)
        _description (str): Descripción del modelo
        _rec_name (str): Campo usado para mostrar y buscar el autor
    """
    _name = 'libro.autor'
    _description = 'Autor de libros'
    _rec_name = 'nombre_y_apellidos'  # Campo usado para mostrar y buscar el autor

    # --- Datos personales del autor ---
    nombre_y_apellidos = fields.Char(
        string='Nombre y apellidos del autor',
        required=True,
        help='Nombre completo del autor'
    )

    fecha_nacimiento = fields.Date(
        string='Fecha de nacimiento',
        required=True,
        help='Fecha de nacimiento del autor'
    )

    nacionalidad = fields.Char(
        string='Nacionalidad',
        help='País de origen del autor'
    )

    biografia = fields.Text(
        string='Biografía',
        help='Información biográfica del autor'
    )

    # --- Relación inversa con libros ---
    # One2many: Un autor puede tener muchos libros
    lista_libros = fields.One2many(
        comodel_name='libro.libro',
        inverse_name='autor_id',
        string='Libros escritos por el autor',
        help='Lista de libros escritos por este autor'
    )
