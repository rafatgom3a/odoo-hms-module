from odoo import models, fields, api

class Department(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(string='Name', required=True)
    capacity = fields.Integer(string='Capacity', default=0)
    is_opened = fields.Boolean(string='Is Opened', default=True)
    patient_ids = fields.One2many('hms.patient', 'department_id', string='Patients')
    
    # Computed field to show current patient count
    patient_count = fields.Integer(string='Current Patients', compute='_compute_patient_count')
    
    @api.depends('patient_ids')
    def _compute_patient_count(self):
        for record in self:
            record.patient_count = len(record.patient_ids)
    
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.name} ({record.patient_count}/{record.capacity})"
            result.append((record.id, name))
        return result