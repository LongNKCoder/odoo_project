from odoo import models, fields, api
from datetime import timedelta, datetime

class ChiPhi(models.Model):
    _name = 'hhd.chiphi'
    name = fields.Char(string = "Tên chi phí", required = True)
    hoadon_ids = fields.One2many("hhd.hoadon", "chiphi_id", String="Hóa dơn")
    loaichiphi = fields.Selection(string="Loại chi phí", selection=[('tiepkhach', 'Tiếp khách'), ('khac', 'Khác'),('dicongtac','Đi công tác') ], required=False, )
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user, string="Nhân viên", required = False, ondelete='set null' )
    doitac_id = fields.Many2one('res.partner', string="Đối tác", required = False, ondelete='set null' )
    invoice_id = fields.Many2one('account.invoice', string="invoice", required=False, ondelete='set null')
    description = fields.Text()
    tong_tien = fields.Float(string="Tổng tiền",  required=False, default=0,compute="_get_total", store=True)
    start_date = fields.Date(string="Ngày bắt đầu", required=False, default= datetime.now().date())
    color = fields.Integer()
    reason = fields.Text(string="Lý do", required=False, )
    trang_thai_state = fields.Selection(string="Trạng thái chi phí",
                                         selection=[('pending', 'Pending'), ('done', 'Done'), ('expried', 'Expried')], default='pending')
    duration = fields.Integer(string="Thời gian tới hạn", required=False, )
    end_date = fields.Date(string="Ngày tới hạn", store=True,
                           compute='_get_end_date', inverse='_set_end_date')
    trang_thai_action = fields.Selection(string="Trạng thái hành động",
                                            selection=[('approve', 'Approve'), ('draft', 'Draft'),
                                                       ('submit', 'Submit'), ('done', 'Done')],
                                            default='draft', track_visibility="onchange")

    def _expried_check(self):
        for chiphi in self.search([]):
            if (chiphi.duration == 0):
                chiphi.trang_thai_state = 'pending'
            if chiphi.trang_thai_state == 'pending' and chiphi.end_date <= datetime.today().date():
                chiphi.trang_thai_state = 'expried'


    @api.depends('hoadon_ids.thanhtien')
    def _get_total(self):
        for chiphi in self:
            comm_total = 0.0
            for hoadon in chiphi.hoadon_ids:
                comm_total += hoadon.thanhtien
            chiphi.update({'tong_tien': comm_total})

    @api.multi
    def action_approve(self):
        self.trang_thai_action = 'approve'

    @api.multi
    def action_submit(self):
        self.trang_thai_action = 'submit'

    @api.multi
    def action_done(self):
        self.trang_thai_action = 'done'
        self.trang_thai_state = 'done'

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = r.start_date + duration

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            r.duration = (r.end_date - r.start_date).days + 1
