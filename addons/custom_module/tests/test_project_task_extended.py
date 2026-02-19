from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestProjectTaskExtended(TransactionCase):

    def setUp(self):
        super(TestProjectTaskExtended, self).setUp()
        self.task_model = self.env['project.task.extended']
        self.tag_model = self.env['project.task.tag']
        self.checklist_model = self.env['project.task.checklist']

    def test_create_task_with_priority(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'priority': '2',
            'estimated_hours': 10.0,
            'actual_hours': 5.0,
        })
        self.assertEqual(task.priority, '2')
        self.assertEqual(task.estimated_hours, 10.0)

    def test_remaining_hours_calculation(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'estimated_hours': 10.0,
            'actual_hours': 3.0,
        })
        self.assertEqual(task.remaining_hours, 7.0)

    def test_remaining_hours_negative(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'estimated_hours': 5.0,
            'actual_hours': 10.0,
        })
        self.assertEqual(task.remaining_hours, 0.0)

    def test_overdue_task(self):
        yesterday = (datetime.now() - timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Overdue Task',
            'deadline': yesterday,
            'state': 'in_progress',
        })
        self.assertTrue(task.is_overdue)

    def test_not_overdue_task(self):
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Future Task',
            'deadline': tomorrow,
        })
        self.assertFalse(task.is_overdue)

    def test_progress_calculation_empty_checklist(self):
        task = self.task_model.create({
            'name': 'Task without checklist',
        })
        self.assertEqual(task.progress_percentage, 0.0)

    def test_progress_calculation_with_checklist(self):
        task = self.task_model.create({
            'name': 'Task with checklist',
        })
        self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 1',
            'is_done': True,
        })
        self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 2',
            'is_done': False,
        })
        self.assertEqual(task.progress_percentage, 50.0)

    def test_negative_estimated_hours_raises_error(self):
        with self.assertRaises(ValidationError):
            self.task_model.create({
                'name': 'Invalid Task',
                'estimated_hours': -5.0,
            })

    def test_negative_actual_hours_raises_error(self):
        with self.assertRaises(ValidationError):
            self.task_model.create({
                'name': 'Invalid Task',
                'actual_hours': -5.0,
            })

    def test_tag_creation(self):
        tag = self.tag_model.create({
            'name': 'Test Tag',
            'color': 1,
        })
        self.assertEqual(tag.name, 'Test Tag')

    def test_checklist_toggle_done(self):
        task = self.task_model.create({
            'name': 'Task for checklist',
        })
        checklist = self.checklist_model.create({
            'task_id': task.id,
            'name': 'Test Item',
            'is_done': False,
        })
        self.assertFalse(checklist.is_done)
        checklist.toggle_done()
        self.assertTrue(checklist.is_done)

    def test_complete_checklist_action(self):
        task = self.task_model.create({
            'name': 'Task for checklist',
        })
        self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 1',
            'is_done': False,
        })
        self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 2',
            'is_done': False,
        })
        task.action_complete_checklist()
        self.assertTrue(all(item.is_done for item in task.checklist_ids))
