from odoo import models
import phonenumbers

from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"
    _name = "res.partner"
    _description = 'E.164 validation of phone field.'

    # Simple check of a phone number. If it is not ambiguous and valid,
    # the phone number is accepted and formatted using the International format.

    def write(self, values):
        phone = values.get('phone')
        if phone:
            try:
                parsed_phone = phonenumbers.parse(phone, None)
            except:
                raise ValidationError(
                    "Phone number has incorrect format. Please enter a E.164 compliant phone number.")
            if not(phonenumbers.is_valid_number(parsed_phone)):
                raise ValidationError(
                    "Phone number has incorrect format. Please enter a E.164 compliant phone number.")
            phone = phonenumbers.format_number(
                parsed_phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        return super(ResPartner, self).write(values)

    def view_related_calls(self):
        # retrieve the user (=aircall user) or partner (=external entity)
        entity = self.env['res.partner'].search(
            [('id', '=', self.env.context.get('partner_id'))], limit=1)
        is_user = len(entity.user_ids) != 0
        return {
            'name': 'Related calls',
            'res_model': 'aircall.call',
            'domain': [("aircall_user_id", "=", entity.user_ids.id)] if is_user else [("external_entity_id", "=", entity.id)],
            'view_id': False,
            'view_mode': 'tree,form',
            'target': 'current',
            'type': 'ir.actions.act_window'
        }
