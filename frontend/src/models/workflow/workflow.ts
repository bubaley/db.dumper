import { type BaseModel } from "../../corexModels/apiModels/baseModel.ts";
import { Config, type ConfigRaw } from "../config/config.ts";

export type WorkflowRaw = {
  id?: number | undefined;
  filename?: string | null;
  active?: boolean;
  status?: string;
  config?: ConfigRaw;
  created_at?: string;
  storage?: string;
};

export class Workflow implements BaseModel {
  id: number | undefined;
  filename: string | null;
  active: boolean;
  status: string;
  createdAt: string | null;
  config: Config;
  storage: string;

  constructor(raw: WorkflowRaw) {
    this.id = raw.id;
    this.storage = raw.storage || "";
    this.filename = raw.filename || null;
    this.active = raw.active || false;
    this.status = raw.status || "";
    this.createdAt = raw.created_at || null;
    this.config = new Config(raw.config || {});
  }

  toJson(): Record<string, any> {
    return {};
  }
}
