from odoo import models, fields

class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    image = fields.Binary(string='Image')
    patient_ids = fields.Many2many('hms.patient', string='Patients')
    
    def name_get(self):
        result = []
        for record in self:
            name = f"Dr. {record.first_name} {record.last_name}"
            result.append((record.id, name))
        return result
