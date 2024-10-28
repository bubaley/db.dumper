import {BaseModel} from "../../corexModels/apiModels/baseModel.ts";

export type WorkflowEventRaw = {
    id?: number | undefined
    name?: string
    is_error?: boolean
    text?: string | null
    created_at?: string | null
}

export class WorkflowEvent implements BaseModel {
    id: number | undefined
    name: string
    isError: boolean
    text: string | null
    createdAt?: string | null


    constructor(raw: WorkflowEventRaw) {
        this.id = raw.id
        this.name = raw.name || ''
        this.isError = raw.is_error || false
        this.text = raw.text || ''
        this.createdAt = raw.created_at || null
    }

    toJson(): Record<string, any> {
        return {}
    }
}
