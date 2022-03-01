# -*- coding: utf-8 -*-
from asyncio.log import logger
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

        logger.warning(json_payload)

        http.request.env["aircall.service"].register(json_payload)

        return
