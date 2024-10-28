import BaseRepo from '@/corexModels/apiModels/baseRepo'
import { s3ConnectionApi } from '@/models/s3Connection/s3ConnectionApi'
import { reactive } from 'vue'
import type { S3Connection } from '@/models/s3Connection/s3Connection'

export class S3ConnectionRepo extends BaseRepo<S3Connection> {
    api = s3ConnectionApi
}

export const s3ConnectionRepo = reactive(new S3ConnectionRepo())
