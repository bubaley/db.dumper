import { configApi } from '@/models/config/configApi'
import { reactive } from 'vue'
import { Workflow, type WorkflowRaw } from '@/models/workflow/workflow'
import BaseRepo from '@/corexModels/apiModels/baseRepo'
import type { Config } from '@/models/config/config'

export class ConfigRepo extends BaseRepo<Config> {
    api = configApi

    async build(config: Config) {
        const result = await this.api.send<WorkflowRaw>({
            method: 'POST',
            action: 'build',
            id: config.id
        })
        return new Workflow(result)
    }
}

export const configRepo = reactive(new ConfigRepo())
