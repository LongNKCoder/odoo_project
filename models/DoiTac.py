from odoo import  models, fields

class DoiTac(models.Model):
    _inherit = 'res.partner'

    doitac = fields.Boolean("DoiTac", default=False)
    chiphi_id = fields.One2many("hhd.chiphi", "doitac_id", String="Doitac", readonly=True)