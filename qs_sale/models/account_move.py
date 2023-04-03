# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    note_client = fields.Char(string="Note", readonly=True)