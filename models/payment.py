from  odoo import  models,api,fields


class HhdPayment(models.Model):
    _inherit = 'account.payment'

    @api.multi
    def action_validate_invoice_payment(self):
        res = super(HhdPayment, self).action_validate_invoice_payment()
        temp = self.env.context.get('active_id')
        invoice = self.env['account.invoice'].browse(temp)
        for chiphi in invoice.chiphi_id:
            chiphi.trang_thai_action = 'done'
            chiphi.trang_thai_state = 'done'
        template = self.env.ref('hhd_cost_recovery.example_email_template')
        self.env['mail.template'].browse(template.id).send_mail(self.id)
        return res