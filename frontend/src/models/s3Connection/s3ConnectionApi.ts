import {S3Connection, S3ConnectionRaw} from './s3Connection.ts';
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";


export class S3ConnectionApi extends BaseModelApi<S3Connection> {
    routeName = 's3_connections'
    fromJson = (json: S3ConnectionRaw) => new S3Connection(json)
}

export const s3ConnectionApi = new S3ConnectionApi();
