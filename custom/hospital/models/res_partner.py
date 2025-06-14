from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient', string='Related Patient')
    vat = fields.Char(string='Tax ID', required=True)

    @api.constrains('email', 'related_patient_id')
    def _check_email_patient_conflict(self):
        for record in self:
            if record.email and record.related_patient_id:
                # Check if the email exists in patient model (excluding the linked patient)
                patient_with_same_email = self.env['hms.patient'].search([
                    ('email', '=', record.email),
                    ('id', '!=', record.related_patient_id.id)
                ])
                if patient_with_same_email:
                    raise ValidationError(
                        f"Cannot link customer with email '{record.email}' "
                        f"because this email already exists in patient model for: "
                        f"{patient_with_same_email[0].first_name} {patient_with_same_email[0].last_name}"
                    )

    def unlink(self):
        # Prevent deletion of customers linked to patients
        for record in self:
            if record.related_patient_id:
                raise UserError(
                    f"Cannot delete customer '{record.name}' because it is linked "
                    f"to patient: {record.related_patient_id.first_name} {record.related_patient_id.last_name}"
                )
        return super(ResPartner, self).unlink()