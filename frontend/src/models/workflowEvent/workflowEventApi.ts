import {WorkflowEvent, type WorkflowEventRaw} from './workflowEvent.ts';
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";


export class WorkflowEventApi extends BaseModelApi<WorkflowEvent> {
    routeName = 'workflow_events'
    fromJson = (json: WorkflowEventRaw) => new WorkflowEvent(json)
}

export const workflowEventApi = new WorkflowEventApi();
