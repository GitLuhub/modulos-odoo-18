from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class TestProjectTaskPro(TransactionCase):

    def setUp(self):
        super(TestProjectTaskPro, self).setUp()
        self.task_model = self.env['project.task']
        self.tag_model = self.env['project.task.tag.pro']
        self.checklist_model = self.env['project.task.checklist.pro']

    def test_create_task_with_estimated_hours(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'estimated_hours': 10.0,
            'actual_hours': 5.0,
        })
        self.assertEqual(task.estimated_hours, 10.0)
        self.assertEqual(task.actual_hours, 5.0)

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

    def test_remaining_hours_zero(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'estimated_hours': 8.0,
            'actual_hours': 8.0,
        })
        self.assertEqual(task.remaining_hours, 0.0)

    def test_overdue_task_in_progress(self):
        yesterday = (datetime.now() - timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Overdue Task',
            'deadline': yesterday,
            'state': 'in_progress',
        })
        self.assertTrue(task.is_overdue)

    def test_overdue_task_open(self):
        yesterday = (datetime.now() - timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Overdue Task',
            'deadline': yesterday,
            'state': 'open',
        })
        self.assertTrue(task.is_overdue)

    def test_not_overdue_task(self):
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Future Task',
            'deadline': tomorrow,
        })
        self.assertFalse(task.is_overdue)

    def test_not_overdue_done_state(self):
        yesterday = (datetime.now() - timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Done Task',
            'deadline': yesterday,
            'state': 'done',
        })
        self.assertFalse(task.is_overdue)

    def test_not_overdue_cancelled_state(self):
        yesterday = (datetime.now() - timedelta(days=1)).date()
        task = self.task_model.create({
            'name': 'Cancelled Task',
            'deadline': yesterday,
            'state': 'cancelled',
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

    def test_progress_calculation_all_done(self):
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
            'is_done': True,
        })
        self.assertEqual(task.progress_percentage, 100.0)

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
        self.assertEqual(tag.color, 1)

    def test_tag_with_default_color(self):
        tag = self.tag_model.create({
            'name': 'Default Tag',
        })
        self.assertEqual(tag.color, 10)

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
        checklist.toggle_done()
        self.assertFalse(checklist.is_done)

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

    def test_task_with_multiple_tags(self):
        tag1 = self.tag_model.create({'name': 'Tag 1', 'color': 1})
        tag2 = self.tag_model.create({'name': 'Tag 2', 'color': 2})
        task = self.task_model.create({
            'name': 'Task with tags',
            'tag_ids': [(4, tag1.id), (4, tag2.id)],
        })
        self.assertEqual(len(task.tag_ids), 2)

    def test_checklist_sequence_order(self):
        task = self.task_model.create({
            'name': 'Task for checklist',
        })
        item3 = self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 3',
            'sequence': 30,
        })
        item1 = self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 1',
            'sequence': 10,
        })
        item2 = self.checklist_model.create({
            'task_id': task.id,
            'name': 'Item 2',
            'sequence': 20,
        })
        checklist_items = task.checklist_ids
        self.assertEqual(checklist_items[0].name, 'Item 1')
        self.assertEqual(checklist_items[1].name, 'Item 2')
        self.assertEqual(checklist_items[2].name, 'Item 3')

    def test_create_task_with_planned_hours(self):
        task = self.task_model.create({
            'name': 'Test Task',
            'planned_hours': 8.0,
        })
        self.assertEqual(task.planned_hours, 8.0)

    def test_planned_hours_default_value(self):
        task = self.task_model.create({
            'name': 'Test Task',
        })
        self.assertEqual(task.planned_hours, 0.0)

    def test_negative_planned_hours_raises_error(self):
        with self.assertRaises(ValidationError):
            self.task_model.create({
                'name': 'Invalid Task',
                'planned_hours': -5.0,
            })
