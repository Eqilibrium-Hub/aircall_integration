from odoo import api, fields, models
import logging
import requests
from datetime import datetime
import base64

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
            'call.ended': self._register_call
        }
        try:
            method = register_map[payload["event"]]
        except KeyError:
            _logger.warning(
                "An unimplemented webhook of type [{}] has been received. Uncheck it in aircall dashboard.".format(payload["event"]))
            return
        method(payload)

    @api.model
    def _register_call(self, payload):
        assert payload["resource"] == "call"
        data = payload["data"]
        duration = 0
        direction = data["direction"]
        started_at = datetime.utcfromtimestamp(int(data["started_at"]))
        external_number = data["raw_digits"]
        aircall_user_id = self.env["res.users"].sudo().search(
            [('phone', 'ilike', data["number"]["digits"])], limit=1).id

        if aircall_user_id is False:
            _logger.warning("Call log matching no one in database. {}/{}/{}".format(
                data["user"]["name"], data["user"]["email"], data["raw_digits"]))
            return

        external_entity = self.env["res.partner"].sudo().search(
            [('phone', 'ilike', external_number)], limit=1).id

        if data["answered_at"] != None and data["answered_at"] != 'None':
            answered_at = datetime.utcfromtimestamp(int(data["answered_at"]))
            ended_at = datetime.utcfromtimestamp(int(data["ended_at"]))
            duration = str(ended_at - answered_at)  # (h:m:s) format

        self._create_audio_attachment(data["voicemail"], "VoiceMail")

        self.env["aircall.call"].sudo().create(
            {
                "aircall_user_id": aircall_user_id,
                "external_entity": external_entity,
                "external_number": external_number,
                "started_at": started_at,
                "duration": duration,
                "direction": direction,
                "recording": self._dl_audio(data["recording"]) if data["recording"] != "None" else False,
                "voicemail": self._dl_audio(data["voicemail"]) if data["voicemail"] != "None" else False
            }
        )

    @api.model
    def _create_audio_attachment(self, url, filename):
        binary_audio = self._dl_audio(url)
        if binary_audio is False:
            return False

        _logger.warning(binary_audio)
        return self.env['ir.attachment'].sudo().create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(binary_audio),
            'mimetype': 'audio/mpeg'
        })

    @staticmethod
    def _dl_audio(url):
        url = "https://file-examples-com.github.io/uploads/2017/11/file_example_MP3_700KB.mp3"
        re = requests.get(url)
        if re.status_code != requests.codes.ok:
            _logger.warning(
                "Could not reach URL to download audio [{}]".format(url))
            return False
        return re.content
