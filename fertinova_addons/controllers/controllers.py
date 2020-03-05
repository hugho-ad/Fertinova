# -*- coding: utf-8 -*-
from odoo import http

# class FertinovaAddons(http.Controller):
#     @http.route('/fertinova_addons/fertinova_addons/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fertinova_addons/fertinova_addons/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fertinova_addons.listing', {
#             'root': '/fertinova_addons/fertinova_addons',
#             'objects': http.request.env['fertinova_addons.fertinova_addons'].search([]),
#         })

#     @http.route('/fertinova_addons/fertinova_addons/objects/<model("fertinova_addons.fertinova_addons"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fertinova_addons.object', {
#             'object': obj
#         })