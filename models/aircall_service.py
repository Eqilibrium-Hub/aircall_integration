import json
from odoo import api, models
import logging
import requests
from datetime import datetime
import base64
import urllib3

_logger = logging.getLogger(__name__)

# http://192.168.1.129:8069/web#id=40&cids=1&menu_id=121&action=146&model=aircall.call&view_type=form
# TODO ? set this as a config parameter

AIRCALL_API_URL = "https://api.aircall.io/v1"


class AircallService(models.TransientModel):
    _name = "aircall.service"
    _description = "Aircall service"

    @api.model
    def validate_webhook_token(self, token):
        true_token = self.env['ir.config_parameter'].sudo(
        ).get_param("aircall.integration_token")

        if true_token is False:
            _logger.warning(
                "Aircall integration token has not been set. Webhooks cannot work without it.")

        return true_token == token

    @api.model
    def get_aircall_api_config(self):
        '''Will throw an error if the config is not set'''
        sudo_param = self.sudo().env['ir.config_parameter']
        return sudo_param.get_param(
            'aircall.api_id'), sudo_param.get_param('aircall.api_token')

    # *********** Parsing methods

    @api.model
    def register(self, payload):
        register_map = {
            'call.created': self._send_insight_card,
            'call.ended': self._register_call,
            'call.tagged': self._register_tags,
            'call.untagged': self._register_tags
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

        external_entity_id = self.env["res.partner"].sudo().search(
            [('phone', 'ilike', external_number)], limit=1).id

        duration = data["duration"]

        self.env["aircall.call"].sudo().create(
            {
                "aircall_user_id": aircall_user_id,
                "id_aircall": data['id'],
                "external_entity_id": external_entity_id,
                "external_number": external_number,
                "started_at": started_at,
                "duration": duration,
                "direction": direction,
                "recording_attachment_id": self._create_audio_attachment(data["recording"], "recording_" + str(started_at.date())) if data["recording"] != None else False,
                "missed_call_reason": data["missed_call_reason"] if data["missed_call_reason"] != None else False
            }
        )

        self._register_tags(payload)

    @api.model
    def _register_tags(self, payload):
        '''Register and overrides tags for an already created 'aircall.call' object.'''
        data = payload["data"]
        tags = [tag["name"] for tag in data["tags"]]
        if tags == []:
            return
        id_aircall = data['id']
        sudo_env = self.env['aircall.tag'].sudo()
        call_record = self.env['aircall.call'].sudo().search(
            [('id_aircall', '=', id_aircall)], limit=1)
        if call_record == False:
            _logger.warning(
                "Could not tag call n°[{}], it was not found in the database.", id_aircall)
            return
        tag_ids = [sudo_env.get_or_create_tag(tag) for tag in tags]
        call_record.tag_ids = [(6, 0, tag_ids)]  # override existing tags

    @api.model
    def _send_insight_card(self, payload):
        api_id, api_token = self.get_aircall_api_config()
        if False in [api_id, api_token]:
            _logger.warning(
                "Aircall api credentials are not set. Some features won't work")
            return

        data = payload['data']

        json_field = self._populate_insight_card(data)
        if json_field is False:
            # Callee was not found on the system on the system
            return

        aircall_url = AIRCALL_API_URL + "/calls/" + \
            str(data['id']) + "/insight_cards"
        req = requests.post(aircall_url, auth=(
            api_id, api_token), json=json_field)

    @api.model
    def _populate_insight_card(self, data):
        sudo = self.sudo()
        callee_entity = sudo.env["res.partner"].search(
            [('phone', 'ilike', data['raw_digits'])], limit=1)
        if callee_entity.id is False:
            return False

        base_url = self.get_base_url()
        params = {
            'id': callee_entity.id,
            'model': 'res.partner',
            'view_type': 'form',
            # We use this trick to get the appropriate menu_id
            'menu_id': sudo.env["ir.ui.menu"].search([('name', '=', "Contacts")], limit=1).id
        }
        json_field = {
            "contents": [
                {
                    "type": "title",
                    "text": "Odoo",
                    "link": base_url
                },
                {
                    "type": "shortText",
                    "label": "Odoo Contact",
                    "text": callee_entity.name,
                    "link": base_url + "#" + urllib3.request.urlencode(params)
                }
            ]
        }
        # Add company line if it is set on the callee
        if callee_entity.company_type == "person" and callee_entity.parent_id != False:
            json_field["contents"].append(
                {
                    "type": "shortText",
                    "label": "Company name",
                    "text": callee_entity.parent_id.name
                }
            )
        _logger.warning(json_field)
        return json_field

    @api.model
    def _create_audio_attachment(self, url, filename):
        binary_audio = self._dl_audio(url)
        if binary_audio is False:
            return False

        return self.env['ir.attachment'].sudo().create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(binary_audio),
            'mimetype': 'audio/mpeg'
        }).id

    @staticmethod
    def _dl_audio(url):  # utils method
        re = requests.get(url)
        if re.status_code != requests.codes.ok:
            _logger.warning(
                "Could not reach URL [{}] to download audio".format(url))
            return False
        return re.content
