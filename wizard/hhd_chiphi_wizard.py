from  odoo import  models,api,fields


class InvoiceChiPhi(models.TransientModel):
    _name = 'hhd.chiphi.wizard'
    user_id = fields.Many2one("res.users", string="nhân viên", required=False, )
    doitac_id = fields.Many2one("res.partner", string="đối tác", required=False, readonly=True)
    chiphi_id = fields.Many2many("hhd.chiphi", relation="chiphi_invoice", string="Chi phí")
    invoice_id = fields.Many2one("account.invoice", string="invoice", required=False, )
    @api.model
    def default_get(self, fields_list):
        defaults = super(InvoiceChiPhi, self).default_get(fields_list)
        if 'active_id' in self._context:
            invoice_id = self.env['account.invoice'].browse(self._context.get('active_id'))
            defaults.update({'doitac_id': invoice_id.partner_id.id, 'invoice_id': invoice_id.id})
        return defaults

    @api.onchange("user_id")
    @api.multi
    def _onchange_1(self):
        return {'domain': {'chiphi_id': [('doitac_id', '=', self.doitac_id.id), ('user_id', '=', self.user_id.id), ('trang_thai_action', '=', 'approve')]}}

    @api.multi
    def save_chiphi(self):
        for chiphi in self.chiphi_id:
            self.invoice_id.chiphi_id = [(4, chiphi.id, 0)]
            if self.env['account.invoice.line'].search_count([('name', '=', chiphi.name)]) < 1:
                self.invoice_id.invoice_line_ids = [
                    (0, 0, {'name': chiphi.name, 'price_unit': chiphi.tong_tien, 'account_id': self.user_id.id})]