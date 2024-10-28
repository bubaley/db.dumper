import BaseRepo from '@/corexModels/apiModels/baseRepo'
import type { Workflow } from '@/models/workflow/workflow'
import { workflowApi } from '@/models/workflow/workflowApi'
import { reactive } from 'vue'

export class WorkflowRepo extends BaseRepo<Workflow> {
    api = workflowApi
    selectedConfig: number | undefined

    async getDownloadUrl(workflow: Workflow) {
        return await this.api.send<{ url: string, filename: string }>({
            method: 'GET',
            action: 'url',
            id: workflow.id
        })
    }
}

export const workflowRepo = reactive(new WorkflowRepo())
