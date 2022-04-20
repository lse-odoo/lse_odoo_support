# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools import dumpstacks

import logging
import random

_logger = logging.getLogger(__name__)

class TechSupportOverrideModuleClass(models.Model):
    _name = 'pos.order'
    _inherit = ['pos.order']

    def track(self, text, vals):
        _logger.info("LSE tracker triggered \n%s \nself %s \nvalues %s",
                        text, self, vals,
                        stack_info=True)
        # dumpstacks()

    @api.model
    def _create(self, data_list):
        r = random.randint(0, 100000)
        _logger.info(f"{r} LSE tracker Call to _create")
        self.track(r, data_list)
        created = super(TechSupportOverrideModuleClass, self)._create(data_list)
        _logger.info(f"{r} after: {self.read(['id', 'name', 'pos_reference'])}")
        return created

    @api.model
    def create(self, vals_list):
        r = random.randint(100000, 200000)
        _logger.info(f"{r} LSE tracker Call to create")
        self.track(r, vals_list)
        created = super(TechSupportOverrideModuleClass, self).create(vals_list)
        _logger.info(f"{r} after: {self.read(['id', 'name', 'pos_reference'])}")
        return created