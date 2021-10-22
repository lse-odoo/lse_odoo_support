# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.tools import dumpstacks

import logging

_logger = logging.getLogger(__name__)

class TechSupportOverrideModuleClass(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order']

    def track(self, vals):
        _logger.warning("LSE tracker triggered \nself %s \nvalues %s",
                        self, vals,
                        stack_info=True)
        # dumpstacks()

    @api.model
    def _create(self, data_list):
        _logger.warning("Call to _create")
        self.track(data_list)
        created = super(TechSupportOverrideModuleClass, self)._create(data_list)
        _logger.warning(created.read(["id", "name"]))
        return created

    @api.model_create_multi
    def create(self, vals_list):
        _logger.warning("Call to create")
        self.track(vals_list)
        created = super(TechSupportOverrideModuleClass, self).create(vals_list)
        _logger.warning(created.read(["id", "name"]))
        return created