from odoo import models, fields, api

class HoaDon(models.Model):
    _name = 'hhd.hoadon'
    name = fields.Char(string = "Tên",required = True)
    thanhtien = fields.Float(string="Thành tiền",  required=True)
    chiphi_id = fields.Many2one('hhd.chiphi', ondelete='cascade', string="Hoa Don Chi Phi", required = True)
    description = fields.Text()