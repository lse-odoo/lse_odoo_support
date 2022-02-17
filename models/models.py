# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools import dumpstacks

import logging
import random

_logger = logging.getLogger(__name__)

class TechSupportOverrideModuleClass(models.Model):
    _name = 'social.account'
    _inherit = ['social.account']

    def track(self, vals):
        _logger.info("LSE tracker triggered \nself %s \nvalues %s",
                        self, vals,
                        stack_info=True)
        # dumpstacks()

    @api.model
    def _write(self, data_list):
        r = random.randint(0, 100000)
        _logger.info(f"{r} LSE tracker Call to _write")
        _logger.info(f"{r} before: {self.read(['id', 'is_media_disconnected'])}")
        self.track(data_list)
        created = super(TechSupportOverrideModuleClass, self)._write(data_list)
        _logger.info(f"{r} after: {self.read(['id', 'is_media_disconnected'])}")
        return created

    def write(self, vals_list):
        r = random.randint(100000, 200000)
        _logger.info(f"{r} LSE tracker Call to write")
        _logger.info(f"{r} before: {self.read(['id', 'is_media_disconnected'])}")
        self.track(vals_list)
        created = super(TechSupportOverrideModuleClass, self).write(vals_list)
        _logger.info(f"{r} after: {self.read(['id', 'is_media_disconnected'])}")
        return created