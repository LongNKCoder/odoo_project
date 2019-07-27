from datetime import datetime

from odoo import models, fields, api

class WizardChiPhi(models.TransientModel):
    _name = 'hhd.wizard'
    _description = "Reason refuse"

    def _default_session(self):
        return self.env['hhd.chiphi'].browse(self._context.get('active_id'))

    reason = fields.Text(string="Lý do", required=False, )
    chiphi_id = fields.Many2one('hhd.chiphi', string="Hoa Don Chi Phi", required = True, default=_default_session)

    @api.multi
    def post_reason(self):
        self.chiphi_id.reason = self.reason
        self.chiphi_id.trang_thai_action = 'draft'
        self.chiphi_id.trang_thai_state = 'pending'
        self.chiphi_id.duration = 0
        return {}
class WizardReport(models.TransientModel):
    _name = 'report.mass.chiphi'

    date_start = fields.Date(string="Start Date", required=True, default=fields.Date.today)
    date_end = fields.Date(string="End Date", required=True, default=fields.Date.today)
    user_id = fields.Many2one(comodel_name="res.users", string="nhân viên", required=False, )
    doitac_id = fields.Many2one(comodel_name="res.partner", string="đối tác", required=False, )
    trang_thai_state = fields.Selection(string="Trạng thái chi phí",
                                        selection=[('pending', 'Pending'), ('done', 'Done'), ('expried', 'Expried')],
                                        default='')
    @api.multi
    def get_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'nhanvien': self.user_id.id,
                'doitac' : self.doitac_id.id,
                'trang_thai_state' : self.trang_thai_state
            },
        }
        return self.env.ref('hhd_cost_recovery.mass_chiphi_report').report_action(self, data=data)

class ReportChiphiCustorm(models.AbstractModel):
    _name = 'report.hhd_cost_recovery.mass_chiphi_report_view'

    @api.model
    def _get_report_values(self, docids, data = None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        nhanvien = data['form']['nhanvien']
        doitac = data['form']['doitac']
        trang_thai_state = data['form']['trang_thai_state']
        docs = []
        domain = [('start_date', '>=', date_start), ('start_date', '<=', date_end)]
        if(nhanvien != False):
            domain.append(('user_id', '=', nhanvien))
        if (doitac != False):
            domain.append(('doitac_id', '=', doitac))
        if (trang_thai_state != False):
            domain.append(('trang_thai_state', '=', trang_thai_state))
        chiphis = self.env['hhd.chiphi'].search(domain)
        for chiphi in chiphis:
            docs.append({
                'chiphi_name': chiphi.name,
                'chiphi_nhanvien': chiphi.user_id,
                'chiphi_tongtien': chiphi.tong_tien,
                'chiphi_doitac': chiphi.doitac_id,
            })
        return dict({'doc_ids': data['ids'],
                         'doc_model': data['model'],
                         'docs': docs
                         })