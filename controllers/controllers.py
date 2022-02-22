# -*- coding: utf-8 -*-
from urllib import request
from odoo import http
import json
import logging

_logger = logging.getLogger(__name__)


class AircallIntegration(http.Controller):

    # Test endpoint
    @http.route('/aircall/hello_world', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/aircall/webhook', auth='public', methods=['POST'], type='json', csrf=False)
    def webhook_listener(self, **kw):
        # we can use this to retrieve json payload directly
        # instead of json-rpc formatted json
        json_payload = dict(http.request.jsonrequest)

        if "token" not in json_payload:
            _logger.warning("Received malformed json payload at webhook endpoint from {}".format(
                http.request.httprequest.environ['REMOTE_ADDR']))
            return

        authentificated = http.request.env['aircall.service'].validate_webhook_token(
            json_payload["token"])
        if not(authentificated):
            _logger.warning("Could not authentificate webhook call from {}".format(
                http.request.httprequest.environ['REMOTE_ADDR']))
            return

        print(json_payload)

        # Request is now identificated, we can parse it safely

        return

    #   print(http.request.httprequest.environ)
    # {'wsgi.version': (1, 0), 'wsgi.url_scheme': 'http', 'wsgi.input': <_io.BufferedReader name=9>, 'wsgi.errors': <_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>, 'wsgi.multithread': True, 'wsgi.multiprocess': False, 'wsgi.run_once': False, 'werkzeug.server.shutdown': <function WSGIRequestHandler.make_environ.<locals>.shutdown_server at 0x7f52f6f339d0>, 'SERVER_SOFTWARE': 'Werkzeug/0.16.1', 'REQUEST_METHOD': 'POST', 'SCRIPT_NAME': '', 'PATH_INFO': '/aircall/webhook', 'QUERY_STRING': '', 'REQUEST_URI': '/aircall/webhook', 'RAW_URI': '/aircall/webhook', 'REMOTE_ADDR': '192.168.1.237', 'REMOTE_PORT': 57785, 'SERVER_NAME': '0.0.0.0', 'SERVER_PORT': '8069', 'SERVER_PROTOCOL': 'HTTP/1.1', 'CONTENT_TYPE': 'application/json', 'HTTP_USER_AGENT': 'PostmanRuntime/7.29.0', 'HTTP_ACCEPT': '*/*', 'HTTP_POSTMAN_TOKEN': 'e32f8f76-76b8-4adc-9ce4-5dbbd5b90fbd', 'HTTP_HOST': '192.168.1.129:8069', 'HTTP_ACCEPT_ENCODING': 'gzip, deflate, br', 'HTTP_CONNECTION': 'keep-alive', 'CONTENT_LENGTH': '76', 'werkzeug.request': <Request 'http://192.168.1.129:8069/aircall/webhook' [POST]>}

    # dir(http.request)

    # ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__enter__', '__eq__', '__exit__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_call_function', '_context',
    #    '_cr', '_env', '_failed', '_handle_exception', '_is_cors_preflight', '_json_response', '_request_type', '_uid', 'auth_method', 'context', 'cr', 'csrf_token', 'db', 'disable_db', 'dispatch', 'endpoint', 'endpoint_arguments', 'env', 'httprequest', 'httpresponse', 'jsonrequest', 'params', 'redirect', 'redirect_query', 'registry', 'registry_cr', 'session', 'set_handler', 'uid', 'validate_csrf']

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
