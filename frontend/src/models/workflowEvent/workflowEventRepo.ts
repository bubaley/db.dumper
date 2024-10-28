import {WorkflowEvent} from './workflowEvent.ts'
import {reactive} from 'vue'
import {workflowEventApi} from "./workflowEventApi.ts";
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";

export class WorkflowEventRepo extends BaseRepo<WorkflowEvent> {
    api = workflowEventApi
}

export const workflowEventRepo = reactive(new WorkflowEventRepo())
