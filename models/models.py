# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.tools import dumpstacks

import logging

_logger = logging.getLogger(__name__)

class TechSupportOverrideModuleClass(models.Model):
    _name = 'mail.channel'
    _inherit = ['mail.channel']

    def track(self, vals):
        value_to_write = vals.get("channel_last_seen_partner_ids", False)
        if value_to_write:
            _logger.warning("LSE tracker triggered",
                            "Self", str(self),
                            "Current value:", self.channel_last_seen_partner_ids,
                            "Updated value:", value_to_write)
            dumpstacks()

    def _write(self, vals):
        self.track(vals)
        return super(TechSupportOverrideModuleClass, self)._write(vals)

    def write(self, vals):
        self.track(vals)
        return super(TechSupportOverrideModuleClass, self).write(vals)