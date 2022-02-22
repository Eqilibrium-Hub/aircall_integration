from odoo import api, fields, models


class aircall_call(models.Model):
    _name = 'aircall.call'
    _description = "aircall call log"

    # replicates some of the fields available through Aircall API
    # https://developer.aircall.io/api-references/#call-overview

    aircall_user_id = fields.Many2one(
        "aircall.user", "Aircall User", readonly=True)

    start_date = fields.Datetime("Start", readonly=True)
    end_date = fields.Datetime("End", readonly=True)
    duration = fields.Integer("Duration", readonly=True)

    inbound_number = fields.Text("Inbound number", readonly=True)
    outbound_number = fields.Text("Outbound number", readonly=True)

    external_entity = fields.Many2one("res.users", readonly=True)

    direction = fields.Selection(
        [("inbound", "Inbound"), ("outbound", "Outbound")], string="res_config_settings_action", readonly=True)

    recording = fields.Binary("Audio Recording", readonly=True)

    missed_call_reason = fields.Selection(
        [("out_of_opening_hours", "Out of opening hours"), ("short_abandoned", "Short abandoned"),
         ("abandonned_in_ivr", "Abandonned in ivr"), (
            "abandoned_in_classic", "Abandoned in classic"),
            ("no_available_agent", "No available agent"), ("agents_did_not_answer", "Agents did not answer")], string="res_config_settings_action", readonly=True)
