from odoo import api, fields, models
import logging
import pytz
from datetime import datetime

# Inspired by https://github.com/odoo/odoo/blob/15.0/addons/google_account/models/google_service.py

_logger = logging.getLogger(__name__)


class AircallService(models.TransientModel):
    _name = "aircall.service"
    _description = "Aircall service"

    @api.model
    def validate_webhook_token(self, token):
        true_token = self.env['ir.config_parameter'].sudo(
        ).get_param("aircall.integration_token")

        if true_token is False:
            _logger.warning(
                "Aircall integration token has not been set. Webhooks cannot function without it.")

        return true_token == token

    # *********** Parsing methods

    @api.model
    def register(self, payload):
        register_map = {
            'call.ended': self.register_call
        }
        try:
            method = register_map[payload["event"]]
        except KeyError:
            _logger.warning(
                "An unimplemented webhook of type [{}] has been received. Uncheck it in aircall dashboard.".format(payload["event"]))
            return
        method(payload)

    @api.model
    def register_call(self, payload):
        assert payload["resource"] == "call"
        data = payload["data"]

        direction = data["direction"]
        duration = 0

        started_at = datetime.utcfromtimestamp(int(data["started_at"]))
        if data["answered_at"] != 'None':
            print(data["answered_at"])
            answered_at = datetime.utcfromtimestamp(int(data["answered_at"]))
            ended_at = datetime.utcfromtimestamp(int(data["ended_at"]))
            duration = str(ended_at - answered_at)  # (h:m:s) format
        # locate aircall user with its email address
        aircall_user_id = self.env["res.users"].sudo().search(
            [('email', 'ilike', data["user"]["email"])], limit=1).id

        if aircall_user_id is False:
            _logger.warning("Call log matching no one in database. {}/{}/{}".format(
                data["user"]["name"], data["user"]["email"], data["raw_digits"]))
            return

        external_number = data["raw_digits"]

        # locate external entity, if it exists, with its number
        external_entity = self.env["res.partner"].search(
            [('phone', '=', external_number)], limit=1).id

        self.env["aircall.call"].sudo().create(
            {
                "aircall_user_id": aircall_user_id,
                "external_entity": external_entity,
                "external_number": external_number,
                "started_at": started_at,
                "duration": duration
            }
        )