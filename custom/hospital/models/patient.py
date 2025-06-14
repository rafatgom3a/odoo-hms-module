from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date
import re

class HmsPatient(models.Model):
    _name = 'hms.patient'
    _description = 'Hospital Management System Patient'

    first_name = fields.Char(string='First Name', required=True)
    last_name = fields.Char(string='Last Name', required=True)
    email = fields.Char(string='Email', required=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age', store=True, readonly=True)
    history = fields.Html(string='History')
    cr_ratio = fields.Float(string='CR Ratio')
    blood_type = fields.Selection([
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-')
    ], string='Blood Type')
    pcr = fields.Boolean(string='PCR')
    image = fields.Binary(string='Image')
    address = fields.Text(string='Address')
    
    # Relations
    department_id = fields.Many2one('hms.department', string='Department', 
                                   domain="[('is_opened', '=', True)]")
    department_capacity = fields.Integer(string='Department Capacity', 
                                        related='department_id.capacity', readonly=True)
    doctor_ids = fields.Many2many('hms.doctor', string='Doctors', 
                                 readonly=True, widget='many2many_tags')
    log_history_ids = fields.One2many('hms.log.history', 'patient_id', string='Log History')
    
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined', required=True)

    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for record in self:
            if record.birth_date:
                record.age = today.year - record.birth_date.year - \
                           ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
            else:
                record.age = 0

    @api.constrains('email')
    def _check_email_validity_and_uniqueness(self):
        for record in self:
            if record.email:
                # Check email format
                email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                if not re.match(email_pattern, record.email):
                    raise ValidationError("Please enter a valid email address.")
                
                # Check uniqueness
                existing = self.search([('email', '=', record.email), ('id', '!=', record.id)])
                if existing:
                    raise ValidationError("This email address is already used by another patient.")

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            # Make doctors field editable when department is selected
            self.doctor_ids = [(5, 0, 0)]  # Clear existing doctors
        else:
            self.doctor_ids = [(5, 0, 0)]  # Clear doctors if no department

    @api.onchange('age', 'birth_date')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': 'PCR Auto-checked',
                    'message': 'PCR field has been automatically checked because age is lower than 30.'
                }
            }

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio(self):
        for record in self:
            if record.pcr and not record.cr_ratio:
                raise ValidationError("CR Ratio is mandatory when PCR is checked.")

    @api.constrains('department_id')
    def _check_department_opened(self):
        for record in self:
            if record.department_id and not record.department_id.is_opened:
                raise ValidationError("You cannot select a closed department.")

    def name_get(self):
        result = []
        for record in self:
            name = f"{record.first_name} {record.last_name}"
            result.append((record.id, name))
        return result