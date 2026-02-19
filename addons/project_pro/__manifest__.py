{
    'name': 'Project Pro',
    'version': '1.0.0',
    'category': 'Project',
    'summary': 'Professional project management with advanced features',
    'description': """
        Project Pro Module
        =================
        
        Advanced project management features:
        - Time tracking (estimated vs actual hours)
        - Deadline management with overdue detection
        - Checklist-based progress tracking
        - Custom tags for categorization
    """,
    'author': 'Your Name',
    'website': 'https://github.com/yourusername/odoo-enterprise-dev',
    'license': 'LGPL-3',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_pro_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
