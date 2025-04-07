import { type BaseModel } from "../../corexModels/apiModels/baseModel.ts";

export type S3ConnectionRaw = {
  id?: number | undefined;
  name?: string;
  url?: string;
  bucket?: string;
  region?: string;
  root?: string;
  access_key?: string;
  secret_key?: string;
};

export class S3Connection implements BaseModel {
  id: number | undefined;
  name: string;
  url: string;
  region: string;
  bucket: string;
  root: string;
  accessKey: string;
  secretKey: string;

  constructor(raw: S3ConnectionRaw) {
    this.id = raw.id;
    this.name = raw.name || "";
    this.url = raw.url || "";
    this.bucket = raw.bucket || "";
    this.region = raw.region || "";
    this.root = raw.root || "";
    this.accessKey = raw.access_key || "";
    this.secretKey = raw.secret_key || "";
  }

  toJson(): Record<string, any> {
    return {
      name: this.name || null,
      url: this.url || null,
      bucket: this.bucket || null,
      region: this.region || null,
      root: this.root || null,
      access_key: this.accessKey || undefined,
      secret_key: this.secretKey || undefined,
    };
  }
}
