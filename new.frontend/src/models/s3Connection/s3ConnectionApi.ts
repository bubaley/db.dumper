import { BaseModelApi } from '@/corexModels/apiModels/baseModelApi'
import {
  S3Connection,
  type S3ConnectionRaw,
} from '@/models/s3Connection/s3Connection'

export class S3ConnectionApi extends BaseModelApi<S3Connection> {
  routeName = 's3_connections'
  fromJson = (json: S3ConnectionRaw) => new S3Connection(json)
}

export const s3ConnectionApi = new S3ConnectionApi()
