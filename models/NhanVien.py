from odoo import  models, fields

class NhanVien(models.Model):
    _inherit = 'res.users'

    nhanvien = fields.Boolean("nhanvien", default=False)
    chiphi_id = fields.One2many("hhd.chiphi", "user_id", String="Nhân Viên", readonly=True)