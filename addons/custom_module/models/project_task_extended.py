from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta




class ProjectTaskExtended(models.Model):
    _name = 'project.task.extended'
    _description = 'Extended Project Task'
    _table = 'project_task_extended'
    _order = 'id desc'

    task_id = fields.Many2one(
        'project.task',
        string='Related Task',
        required=True,
        ondelete='cascade'
    )

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Medium'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='1', index=True)

    estimated_hours = fields.Float(string='Estimated Hours')
    actual_hours = fields.Float(string='Actual Hours')
    remaining_hours = fields.Float(
        string='Remaining Hours',
        compute='_compute_remaining_hours',
        store=True
    )

    deadline = fields.Date(string='Deadline')
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_is_overdue',
        store=True
    )

    checklist_ids = fields.One2many(
        'project.task.checklist',
        'task_id',
        string='Checklist'
    )

    progress_percentage = fields.Float(
        string='Progress %',
        compute='_compute_progress',
        store=True
    )

    tag_ids = fields.Many2many(
        'project.task.tag',
        'project_task_extended_tag_rel',
        'extended_task_id',
        'tag_id',
        string='Tags'
    )

    @api.depends('estimated_hours', 'actual_hours')
    def _compute_remaining_hours(self):
        for record in self:
            record.remaining_hours = max(
                0,
                record.estimated_hours - record.actual_hours
            )

    @api.depends('deadline', 'task_id.state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for record in self:
            record.is_overdue = (
                record.deadline and
                record.deadline < today and
                record.task_id.state not in ['done', 'cancelled']
            )

    @api.depends('checklist_ids', 'checklist_ids.is_done')
    def _compute_progress(self):
        for record in self:
            if not record.checklist_ids:
                record.progress_percentage = 0.0
            else:
                done_count = len(record.checklist_ids.filtered('is_done'))
                total_count = len(record.checklist_ids)
                record.progress_percentage = (done_count / total_count) * 100

    @api.constrains('estimated_hours', 'actual_hours')
    def _check_hours(self):
        for record in self:
            if record.estimated_hours < 0:
                raise ValidationError(_('Estimated hours cannot be negative'))
            if record.actual_hours < 0:
                raise ValidationError(_('Actual hours cannot be negative'))

    def action_complete_checklist(self):
        self.ensure_one()
        for checklist in self.checklist_ids:
            checklist.is_done = True
        return True


class ProjectTaskChecklist(models.Model):
    _name = 'project.task.checklist'
    _description = 'Task Checklist Item'
    _order = 'sequence'

    task_id = fields.Many2one(
        'project.task.extended',
        string='Task',
        required=True,
        ondelete='cascade'
    )

    name = fields.Char(string='Description', required=True)
    is_done = fields.Boolean(string='Done', default=False)
    sequence = fields.Integer(string='Sequence', default=10)

    def toggle_done(self):
        self.ensure_one()
        self.is_done = not self.is_done
        return True


class ProjectTaskTag(models.Model):
    _name = 'project.task.tag'
    _description = 'Task Tag'
    _order = 'name'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color', default=10)
