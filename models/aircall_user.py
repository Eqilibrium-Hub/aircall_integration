from odoo import api, fields, models
from odoo.exceptions import ValidationError


class aircall_user(models.Model):
    _name = 'aircall.user'
    _description = "aircall user model"

    _sql_constraints = [
        ('unique_aircall_user_id', 'unique(aircall_user_id)',
         'aircall id has to be unique'),
        ('unique_internal_user_id', 'unique(internal_user_id)',
         'this internal user has already been assigned a number')
    ]

    # Each Aircall user is linked to a res.user
    # In particular the res.user HAS to be an internal user

    aircall_user_id = fields.Integer("Aircall Id")
    aircall_phone_number = fields.Char("Aircall phone number", size=30)
    internal_user_id = fields.Many2one(
        "res.users", string='Internal user', domain=lambda self: [('groups_id', 'in', self.env.ref('base.group_user').id)])

    # Can't contrains on the specific group field of res.users

    @api.constrains('internal_user_id')
    def user_is_internal_user(self):
        for record in self:
            if (not self.internal_user_id.has_group('base.group_user')):
                raise ValidationError("User has to be internal")
