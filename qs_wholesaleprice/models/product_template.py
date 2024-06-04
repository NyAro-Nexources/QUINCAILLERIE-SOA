# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    wholesaleprice = fields.Float(
        string="Prix de gros", compute="_compute_wholesaleprice"
    )

    def _compute_wholesaleprice(self):
        product_pricelist = self.env["product.pricelist"].search([])
        for pricelist in product_pricelist:
            if pricelist.name.lower() == "pv gros" and pricelist.active == True:
                for product in self:
                        product_pricelist_item = self.env["product.pricelist.item"].search(
                            [("product_tmpl_id", "=", product.id), ("pricelist_id", "=", pricelist.id)]
                        )
                        if product_pricelist_item:
                            for product_item in product_pricelist_item:
                                product.wholesaleprice = product_item.fixed_price
                        else:
                            product.wholesaleprice = False
