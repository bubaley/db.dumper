import { type BaseModel } from "../../corexModels/apiModels/baseModel.ts";

export type DatabaseConnectionRaw = {
  id?: number | undefined;
  host?: string;
  port?: number;
  db?: string;
  user?: string;
  password?: string;
  type?: string;
};

export class DatabaseConnection implements BaseModel {
  id: number | undefined;
  host: string;
  port: number | null;
  db: string;
  user: string;
  password: string;
  type?: string;

  constructor(raw: DatabaseConnectionRaw) {
    this.id = raw.id;
    this.host = raw.host || "";
    this.port = raw.port || null;
    this.db = raw.db || "";
    this.user = raw.user || "";
    this.password = raw.password || "";
    this.type = raw.type || "postgres";
  }

  toJson(): Record<string, any> {
    return {
      type: this.type,
      host: this.host || undefined,
      port: this.port || undefined,
      db: this.db || null,
      user: this.user || undefined,
      password: this.password || undefined,
    };
  }
}
