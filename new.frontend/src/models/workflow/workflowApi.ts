import { Workflow, type WorkflowRaw } from './workflow'
import {BaseModelApi} from "@/corexModels/apiModels/baseModelApi";


export class WorkflowApi extends BaseModelApi<Workflow> {
    routeName = 'workflows'
    fromJson = (json: WorkflowRaw) => new Workflow(json)
}

export const workflowApi = new WorkflowApi();
