from odoo import api, fields, models


class aircall_tag(models.Model):
    _name = 'aircall.tag'
    _description = "aircall tag on calls"

    name = fields.Char("Tag name")

    @api.model
    def get_or_create_tag(self, tag_char):
        sudo_env = self.env['aircall.tag'].sudo()
        res = sudo_env.search([('name', '=', tag_char)], limit=1)
        if res.id != False:
            return res.id
        return sudo_env.create(
            {
                'name': tag_char
            }
        ).id
