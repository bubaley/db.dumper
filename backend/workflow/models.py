from django.db import models


class Workflow(models.Model):
    class Storage(models.TextChoices):
        LOCAL = 'local'
        S3 = 's3'

    class Status(models.TextChoices):
        CREATED = 'created'
        IN_PROGRESS = 'in_progress'
        FAILED = 'failed'
        DONE = 'done'

    ACTIVE_STATUSES = [Status.CREATED, Status.IN_PROGRESS]

    filename = models.CharField(max_length=255, null=True)
    config = models.ForeignKey('config.Config', on_delete=models.CASCADE, related_name='workflows')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.CREATED, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=False)
    storage = models.CharField(choices=Storage.choices, max_length=16)

    class Meta:
        ordering = ['-created_at']


class WorkflowEvent(models.Model):
    workflow = models.ForeignKey('Workflow', on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=128)
    text = models.TextField(null=True)
    is_error = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
