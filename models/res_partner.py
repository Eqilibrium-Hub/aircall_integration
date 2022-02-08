from odoo import api, fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'

    aircall_phone_number = fields.Char(
        string="Aircall number ☎️", readonly=True, compute="_compute_aircall_phone_number")

    def _compute_aircall_phone_number(self):
        res = self.user_ids.mapped('aircall_phone_number')
        if res != []:
            self.aircall_phone_number = res[0]
        else:
            self.aircall_phone_number = False
