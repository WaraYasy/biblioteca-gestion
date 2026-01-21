# -*- coding: utf-8 -*-
# from odoo import http


# class BibliotecaGestion(http.Controller):
#     @http.route('/biblioteca_gestion/biblioteca_gestion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/biblioteca_gestion/biblioteca_gestion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('biblioteca_gestion.listing', {
#             'root': '/biblioteca_gestion/biblioteca_gestion',
#             'objects': http.request.env['biblioteca_gestion.biblioteca_gestion'].search([]),
#         })

#     @http.route('/biblioteca_gestion/biblioteca_gestion/objects/<model("biblioteca_gestion.biblioteca_gestion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biblioteca_gestion.object', {
#             'object': obj
#         })

