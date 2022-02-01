# -*- coding: utf-8 -*-
# from odoo import http


# class AircallIntegration(http.Controller):
#     @http.route('/aircall_integration/aircall_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aircall_integration/aircall_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('aircall_integration.listing', {
#             'root': '/aircall_integration/aircall_integration',
#             'objects': http.request.env['aircall_integration.aircall_integration'].search([]),
#         })

#     @http.route('/aircall_integration/aircall_integration/objects/<model("aircall_integration.aircall_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aircall_integration.object', {
#             'object': obj
#         })
