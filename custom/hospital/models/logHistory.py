from odoo import models, fields

class LogHistory(models.Model):
    _name = 'hms.log.history'
    _description = 'Patient Log History'
    _order = 'date desc'

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True, ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user, required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    description = fields.Text(string='Description', required=True)