from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProjectTaskPro(models.Model):
    _name = 'project.task'
    _inherit = 'project.task'

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
        'project.task.checklist.pro',
        'task_id',
        string='Checklist'
    )

    progress_percentage = fields.Float(
        string='Progress %',
        compute='_compute_progress',
        store=True
    )

    tag_ids = fields.Many2many(
        'project.task.tag.pro',
        'task_tag_pro_rel',
        'task_id',
        'tag_id',
        string='Tags'
    )

    @api.depends('estimated_hours', 'actual_hours')
    def _compute_remaining_hours(self):
        for task in self:
            task.remaining_hours = max(0, task.estimated_hours - task.actual_hours)

    @api.depends('deadline', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.today()
        for task in self:
            task.is_overdue = (
                task.deadline and
                task.deadline < today and
                task.state not in ['done', 'cancelled']
            )

    @api.depends('checklist_ids', 'checklist_ids.is_done')
    def _compute_progress(self):
        for task in self:
            if not task.checklist_ids:
                task.progress_percentage = 0.0
            else:
                done_count = len(task.checklist_ids.filtered('is_done'))
                total_count = len(task.checklist_ids)
                task.progress_percentage = (done_count / total_count) * 100

    @api.constrains('estimated_hours', 'actual_hours')
    def _check_hours(self):
        for task in self:
            if task.estimated_hours < 0:
                raise ValidationError('Estimated hours cannot be negative')
            if task.actual_hours < 0:
                raise ValidationError('Actual hours cannot be negative')

    def action_complete_checklist(self):
        self.ensure_one()
        for checklist in self.checklist_ids:
            checklist.is_done = True
        return True


class ProjectTaskChecklistPro(models.Model):
    _name = 'project.task.checklist.pro'
    _description = 'Task Checklist Pro'
    _order = 'sequence'

    task_id = fields.Many2one(
        'project.task',
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


class ProjectTaskTagPro(models.Model):
    _name = 'project.task.tag.pro'
    _description = 'Task Tag Pro'
    _order = 'name'

    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color', default=10)
