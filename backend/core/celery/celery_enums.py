import enum


class CeleryTaskQueues(enum.StrEnum):
    LOW = 'low'
    DEFAULT = 'default'
    URGENT = 'urgent'


class CeleryTasks(enum.StrEnum):
    WORKFLOW_INIT = 'workflow.init'
    USER_EXAMPLE = 'user.example'
