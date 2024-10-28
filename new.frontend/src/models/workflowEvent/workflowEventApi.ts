import { BaseModelApi } from '@/corexModels/apiModels/baseModelApi'
import { WorkflowEvent,type  WorkflowEventRaw } from '@/models/workflowEvent/workflowEvent'


export class WorkflowEventApi extends BaseModelApi<WorkflowEvent> {
    routeName = 'workflow_events'
    fromJson = (json: WorkflowEventRaw) => new WorkflowEvent(json)
}

export const workflowEventApi = new WorkflowEventApi();
