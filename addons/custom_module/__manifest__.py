{
    'name': 'Project Management',
    'version': '1.0.0',
    'category': 'Project',
    'summary': 'Custom project and task management module',
    'description': """
        Project Management Module for Odoo
        ==================================
        
        This custom module demonstrates:
        - Custom Python models with Odoo ORM
        - XML views (form, tree, kanban)
        - Access control and security
        - Workflow automation
        - Unit tests
    """,
    'author': 'Your Name',
    'website': 'https://github.com/yourusername/odoo-enterprise-dev',
    'license': 'LGPL-3',
    'depends': ['base', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_task_views.xml',
        'views/project_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
