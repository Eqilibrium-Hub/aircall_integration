from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # HTTP Basic Authentification for Aircall API
    api_id = fields.Char("api id")
    api_token = fields.Char("api token")

    # Integration token used to validate incoming webhook calls
    integration_token = fields.Char("integration token")

    delete_after = fields.Integer("delete call logs after x days")
    cron_delete = fields.Boolean("periodically delete call logs")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        env = self.env['ir.config_parameter'].sudo()
        res["api_id"] = env.get_param('aircall.api_id', default="")
        res["api_token"] = env.get_param('aircall.api_token', default="")
        res["integration_token"] = env.get_param(
            'aircall.integration_token', default="")
        res["delete_after"] = env.get_param(
            'aircall.delete_after')
        res["cron_delete"] = env.get_param(
            'aircall.cron_delete')
        return res

    @api.model
    def set_values(self):
        env = self.env['ir.config_parameter'].sudo()

        if self.delete_after <= 0:
            raise ValidationError("Call logging field can't be negative.")

        env.set_param('aircall.api_id', self.api_id)
        env.set_param('aircall.api_token', self.api_token)
        env.set_param('aircall.integration_token', self.integration_token)
        env.set_param('aircall.delete_after', self.delete_after)
        env.set_param('aircall.cron_delete', self.cron_delete)
        super(ResConfigSettings, self).set_values()
