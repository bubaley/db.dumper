import {Workflow, WorkflowRaw} from './workflow.ts';
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";


export class WorkflowApi extends BaseModelApi<Workflow> {
    routeName = 'workflows'
    fromJson = (json: WorkflowRaw) => new Workflow(json)
}

export const workflowApi = new WorkflowApi();
