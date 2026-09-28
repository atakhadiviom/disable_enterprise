# -*- coding: utf-8 -*-
# Copyright (C) 2024-Today: Odoo Community Iran
# @author: Odoo Community Iran (https://odoo-community.ir/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import logging
from datetime import datetime, timedelta

from odoo import fields
from odoo.models import AbstractModel

_logger = logging.getLogger(__name__)


def add_years(today, years):
    """Return a datetime that's `years` years after `today`.

    Same calendar date in the destination year when it exists
    (Feb 29 -> Feb 28 on non-leap years via timedelta fallback).
    """
    try:
        return today.replace(year=today.year + years)
    except ValueError:
        # Feb 29 -> non-leap year: fall back to +365 days per year
        return today + timedelta(days=365 * years)


class PublisherWarrantyContract(AbstractModel):
    _inherit = "publisher_warranty.contract"

    def _get_message(self):
        # Never phone home: send an empty payload.
        super()._get_message()
        return {}

    def update_notification(self, cron_mode=True):
        """Neutralize Odoo's publisher warranty callback.

        Runs after the original (which may set expiration from
        enterprise_info) and pushes the expiration one year forward
        with a dummy enterprise code.
        """
        res = super().update_notification(cron_mode)
        expiration_date = fields.Datetime.to_string(add_years(datetime.now(), 1))
        expiration_reason = 'nothing'
        try:
            set_str = self.env['ir.config_parameter'].sudo().set_str
            set_str('database.expiration_date', expiration_date)
            set_str('database.expiration_reason', expiration_reason)
            set_str('database.enterprise_code', "ABC")
            _logger.info('Disable Enterprise by Date: %s, reason: %s', expiration_date, expiration_reason)
        except Exception:
            _logger.debug("Exception while change expiration_date", exc_info=True)
        return res
