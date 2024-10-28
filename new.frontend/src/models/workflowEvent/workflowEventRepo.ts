import BaseRepo from '@/corexModels/apiModels/baseRepo'
import type { WorkflowEvent } from '@/models/workflowEvent/workflowEvent'
import { workflowEventApi } from '@/models/workflowEvent/workflowEventApi'
import { reactive } from 'vue'

export class WorkflowEventRepo extends BaseRepo<WorkflowEvent> {
    api = workflowEventApi
}

export const workflowEventRepo = reactive(new WorkflowEventRepo())
