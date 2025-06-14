{
    'name': 'Hospital Management System',
    'category': 'Healthcare',
    'summary': 'Manage hospital operations including patients, doctors, and departments',
    'description': """
        Hospital Management System
        ==========================
        This module provides functionality to manage:
        - Patients with medical history, states, and email validation
        - Doctors with patient assignments
        - Departments with capacity management
        - Log history tracking for patients
        - CRM integration with customer-patient linking
        - Email validation and uniqueness constraints
        - Auto-calculated age based on birth date
            """,
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/patient_views.xml',
        'views/department_views.xml',
        'views/doctor_views.xml',
        'views/menu_views.xml',
        'views/crm_customer_views.xml',
    ],
}
