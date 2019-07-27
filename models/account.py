from  odoo import  models,api,fields


class HhdInvoice(models.Model):
    _inherit = 'account.invoice'
    chiphi_id = fields.One2many("hhd.chiphi", "invoice_id", String="Invoice", readonly=True)