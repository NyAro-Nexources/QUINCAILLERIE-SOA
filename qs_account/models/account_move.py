#-*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import date, datetime, time


class AccountMove(models.Model):
    _inherit = 'account.move'

    # delivery_time = fields.Float(string='Delivery Time')
    is_charge = fields.Boolean()
    is_spec = fields.Boolean(string="is_spec", compute="_compute_is_spec")
    journal_paie_types = fields.Char(compute='journal_types_compute')
    # payment_paie_date = fields.Date(compute='journal_name_compute', store=True, string="payment date")
    payment_paie_date = fields.Date(compute='journal_name_compute')
    # communication = fields.Char(compute='journal_name_compute', store=True)  self.env["account.payment"].search([('ref', '=', 'FAC/2023/01626')]).journal_id.name
    about_payment = fields.Char(compute='_compute_about_payment')


    def journal_types_compute(self):
        for rec in self:
            rec.journal_paie_types = False
            json_values = rec._get_reconciled_info_JSON_values()
            if json_values:
                rec.journal_paie_types = ', '.join(val.get('journal_name', '') for val in json_values)


    def journal_name_compute(self):
        for rec in self:
            rec.payment_paie_date = False
            json_values = rec._get_reconciled_info_JSON_values()
            if json_values:
                rec.payment_paie_date = json_values[0]['date']

            # invoice_to_w = self.env["account.move"].search([('name', '=', rec.ref)])
            # invoice_to_w.write({"payment_paie_date": rec.payment_id.date})


    def _compute_about_payment(self):
        for rec in self:
            rec.about_payment = False
            json_values = rec._get_reconciled_info_JSON_values()
            if json_values:
                # rec.about_payment = ', '.join(val.get('ref', '') for val in json_values)
                if rec._get_reconciled_info_JSON_values()[0]['payment_id']:
                    rec.about_payment = self.env['account.payment'].search([('id', '=', rec._get_reconciled_info_JSON_values()[0]['account_payment_id'])]).ref




    @api.depends()
    def _compute_is_spec(self):
        self.is_spec = self.env.user.has_group('qs_account.group_account_user_spec')

    @api.model
    def get_spec(self):
        return self.env.user.has_group('qs_account.group_account_user_spec')