# -*- coding: utf-8 -*-

{
    'name': 'DAS Base',
    'version': '1.0',
    'category': 'Hidden',
    'description': """
DAS Base  
========
""",
    'depends': ['base', 'hr', 'project', 'report_xlsx', 'web', 'web_gantt', 'web_dashboard', 'ks_dashboard_ninja'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
