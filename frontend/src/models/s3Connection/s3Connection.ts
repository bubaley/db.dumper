import {BaseModel} from "../../corexModels/apiModels/baseModel.ts";

export type S3ConnectionRaw = {
    id?: number | undefined
    name?: string
    url?: string
    bucket?: string
    region?: string
    root?: string
}

export class S3Connection implements BaseModel {
    id: number | undefined
    name: string
    url: string
    region: string
    bucket: string
    root: string

    constructor(raw: S3ConnectionRaw) {
        this.id = raw.id
        this.name = raw.name || ''
        this.url = raw.url || ''
        this.bucket = raw.bucket || ''
        this.region = raw.region || ''
        this.root = raw.root || ''
    }

    toJson(): Record<string, any> {
        return {}
    }
}
