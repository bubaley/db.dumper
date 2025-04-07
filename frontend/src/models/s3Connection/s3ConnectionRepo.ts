import { S3Connection } from "./s3Connection.ts";
import { reactive } from "vue";
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";
import { s3ConnectionApi } from "./s3ConnectionApi.ts";

export class S3ConnectionRepo extends BaseRepo<S3Connection> {
  api = s3ConnectionApi;
  routeKey = "s3";

  defaultItem() {
    return new S3Connection({});
  }
}

export const s3ConnectionRepo = reactive(new S3ConnectionRepo());
