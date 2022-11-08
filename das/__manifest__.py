# -*- coding: utf-8 -*-

{
    'name': 'ePlanning-IT',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
DAS Management  
==============
""",
    'depends': ['das_base', 'das_project', 'das_hr', 'web_gantt'],
    'data': [
        'data/ir_cron.xml',
        'data/data_fictional_planning.xml',
        'security/das_security.xml',
        'security/ir.model.access.csv',
        'views/das_category_views.xml',
        'views/das_category_type_views.xml',
        'views/das_locality_views.xml',
        'wizard/planning_division_wizard.xml',
        'wizard/availability_filter_wizard.xml',
        'wizard/planning_fictional_wizard.xml',
        'views/das_account_views.xml',
        'views/das_account_reference.xml',
        'views/das_planning_views.xml',
        'views/das_planning_date_views.xml',
        'views/das_fictional_views.xml',
        'views/das_fictional_batch_views.xml',
        'views/das_analyse_views.xml',
        'views/res_availability_views.xml',
        'views/res_config_settings_views.xml',
        'views/hr_employee_views.xml',
        'views/project_project_views.xml',
        'views/das_planning_menus.xml',
        'report/report.xml'
    ],
    'qweb': [
        "static/src/xml/*.xml",
    ],
    'assets': {
        'web.assets_backend': [
            'das/static/src/js/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
