from email.policy import default
from odoo import api, fields, models


class res_users(models.Model):
    _inherit = 'res.users'
    _name = 'res.users'

    # @property
    # def SELF_READABLE_FIELDS(self):
    #     """ The list of fields a user can read on their own user record.
    #     In order to add fields, please override this property on model extensions.
    #     """
    #     return super().SELF_READABLE_FIELDS + ["aircall_user_ids" + "aircall_phone_number"]

    # @property
    # def SELF_WRITEABLE_FIELDS(self):
    #     """ The list of fields a user can write on their own user record.
    #     In order to add fields, please override this property on model extensions.
    #     """
    #     return super().SELF_WRITEABLE_FIELDS + ["aircall_user_ids" + "aircall_phone_number"]

    # One2many but it is actually a One2One
    aircall_user_ids = fields.One2many(
        'aircall.user', 'internal_user_id', readonly=True, invisible=True)

    aircall_phone_number = fields.Text(
        "Aircall ID ☎️", compute="_compute_aircall_phone_number", readonly=True, default="+65")

    @api.depends("aircall_user_ids.aircall_phone_number")
    def _compute_aircall_phone_number(self):
        for record in self:
            id = record.aircall_user_ids.mapped(
                lambda x: x.aircall_phone_number)
            if id != []:
                record.aircall_phone_number = id[0]
            else:
                record.aircall_phone_number = False
