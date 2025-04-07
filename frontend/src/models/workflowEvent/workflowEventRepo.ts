import { WorkflowEvent } from "./workflowEvent.ts";
import { reactive } from "vue";
import { workflowEventApi } from "./workflowEventApi.ts";
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";
import type { BaseModel } from "../../corexModels/apiModels/baseModel.ts";

export class WorkflowEventRepo extends BaseRepo<WorkflowEvent> {
  api = workflowEventApi;

  defaultItem(): BaseModel {
    return new WorkflowEvent({});
  }
}

export const workflowEventRepo = reactive(new WorkflowEventRepo());
