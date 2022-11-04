# -*- coding: utf-8 -*-

{
    'name': 'DAS Human resource',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
Configure HR module to DAS (Domaine d'Activité Stratégique)
===========================================================
""",
    'depends': ['das_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/hr_department_views.xml',
        'views/hr_job_views.xml',
        'views/hr_job_type_views.xml'
    ],
    'application': False,
    'installable': True,
    'license': 'LGPL-3',
}
