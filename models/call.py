from email.policy import default
from odoo import api, fields, models


class aircall_call(models.Model):
    _name = 'aircall.call'
    _description = "aircall call log"

    # replicates some of the fields available through Aircall API
    # https://developer.aircall.io/api-references/#call-overview

    aircall_user_id = fields.Many2one(
        "res.users", "Aircall User", readonly=True)
    external_entity = fields.Many2one("res.partner", readonly=True)

    started_at = fields.Datetime("Start", readonly=True)
    duration = fields.Char("Duration", readonly=True, default='0')

    external_number = fields.Char("Outbound number", readonly=True)

    direction = fields.Selection(
        [("inbound", "Inbound"), ("outbound", "Outbound")], string="Type", readonly=True)

    recording = fields.Binary("Audio Recording", readonly=True)

    missed_call_reason = fields.Selection(
        [("out_of_opening_hours", "Out of opening hours"), ("short_abandoned", "Short abandoned"),
         ("abandonned_in_ivr", "Abandonned in ivr"), (
            "abandoned_in_classic", "Abandoned in classic"),
            ("no_available_agent", "No available agent"), ("agents_did_not_answer", "Agents did not answer")], string="Missed call reason", readonly=True)
