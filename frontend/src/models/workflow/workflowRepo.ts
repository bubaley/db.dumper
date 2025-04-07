import { Workflow } from "./workflow.ts";
import { reactive } from "vue";
import { workflowApi } from "./workflowApi.ts";
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";
import type { BaseModel } from "../../corexModels/apiModels/baseModel.ts";

export class WorkflowRepo extends BaseRepo<Workflow> {
  api = workflowApi;
  selectedConfig: number | undefined;
  routeKey = "workflow";

  defaultItem(): BaseModel {
    return new Workflow({});
  }

  async getDownloadUrl(workflow: Workflow) {
    return await this.api.send<{ url: string; filename: string }>({
      method: "GET",
      action: "url",
      id: workflow.id,
    });
  }
}

export const workflowRepo = reactive(new WorkflowRepo());
