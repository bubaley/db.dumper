import { Config } from "./config.ts";
import { reactive } from "vue";
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";
import { configApi } from "./configApi.ts";
import { Workflow, type WorkflowRaw } from "../workflow/workflow.ts";

export class ConfigRepo extends BaseRepo<Config> {
  api = configApi;
  routeKey = "config";

  defaultItem() {
    return new Config({});
  }

  async build(config: Config) {
    const result = await this.api.send<WorkflowRaw>({
      method: "POST",
      action: "build",
      id: config.id,
    });
    return new Workflow(result);
  }
}

export const configRepo = reactive(new ConfigRepo());
