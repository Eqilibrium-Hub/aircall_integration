from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # HTTP Basic Authentification for Aircall API
    api_id = fields.Char("api id")
    api_token = fields.Char("api token")

    # Integration token used to validate incoming webhook calls
    integration_token = fields.Char("integration token")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        env = self.env['ir.config_parameter'].sudo()
        res["api_id"] = env.get_param('aircall.api_id', default="")
        res["api_token"] = env.get_param('aircall.api_token', default="")
        res["integration_token"] = env.get_param(
            'aircall.integration_token', default="")
        return res

    @api.model
    def set_values(self):
        env = self.env['ir.config_parameter'].sudo()
        env.set_param('aircall.api_id', self.api_id)
        env.set_param('aircall.api_token', self.api_token)
        env.set_param('aircall.integration_token', self.integration_token)
        super(ResConfigSettings, self).set_values()
