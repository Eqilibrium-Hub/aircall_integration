from odoo import models
import phonenumbers

from odoo.exceptions import ValidationError


class Partners(models.Model):
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
        return super(Partners, self).write(values)
