from odoo import api, fields, models
import logging

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
