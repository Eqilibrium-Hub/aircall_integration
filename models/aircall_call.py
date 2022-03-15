from odoo import api, fields, models
from datetime import datetime, timedelta

import logging
_logger = logging.getLogger(__name__)


class AircallCall(models.Model):
    _name = 'aircall.call'
    _description = "aircall call log"

    # replicates some of the fields available through Aircall API
    # https://developer.aircall.io/api-references/#call-overview

    name = fields.Char(compute="_compute_name", store=True)
    id_aircall = fields.Char(invisible=1)
    tag_ids = fields.Many2many(
        "aircall.tag", "tag", string="Tags which the agent assigned to the call")
    aircall_user_id = fields.Many2one(
        "res.users", "Aircall User", readonly=True)
    external_entity_id = fields.Many2one("res.partner", readonly=True)

    started_at = fields.Datetime("Start", readonly=True)
    duration = fields.Char("Duration", readonly=True,
                           help="Duration of the call in seconds.")
    external_number = fields.Char("Outbound number", readonly=True)
    direction = fields.Selection(
        [("inbound", "Inbound"), ("outbound", "Outbound")], string="Type", readonly=True)
    # we have to create an attachment since you can't set a mime type on a raw binary field
    recording_attachment_id = fields.Many2one('ir.attachment',
                                              string="Audio Recording", ondelete='set null', readonly=True)
    recording = fields.Binary(
        related="recording_attachment_id.datas", attachment=False, readonly=True)
    missed_call_reason = fields.Selection(
        [("out_of_opening_hours", "Out of opening hours"), ("short_abandoned", "Short abandoned"),
         ("abandonned_in_ivr", "Abandonned in ivr"), (
            "abandoned_in_classic", "Abandoned in classic"),
            ("no_available_agent", "No available agent"), ("agents_did_not_answer", "Agents did not answer")], string="Missed call reason", readonly=True)

    @api.depends("aircall_user_id.name", "started_at")
    def _compute_name(self):
        for call in self:
            call.name = "{} on {}".format(call.aircall_user_id.name,
                                          call.started_at.date())

    @api.model
    def _cron_destroy_expired_calls(self):
        destroy_flag = self.env['ir.config_parameter'].sudo(
        ).get_param('aircall.cron_delete')
        if destroy_flag == False:
            return
        delete_after = self.env['ir.config_parameter'].sudo().get_param(
            'aircall.delete_after')
        expiry_date = (datetime.utcnow(
        ) - timedelta(hours=int(delete_after))).strftime("%Y/%m/%d, %H:%M:%S")
        self.env['aircall.call'].sudo().search(
            [('started_at', '<', expiry_date)]).unlink()

    def unlink(self):
        '''Since recording attachment is not a field, we need to delete it as well.'''
        for call in self:
            call.recording_attachment_id.unlink()
        return super(AircallCall, self).unlink()
