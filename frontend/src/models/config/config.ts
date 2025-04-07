import { type BaseModel } from "../../corexModels/apiModels/baseModel.ts";
import {
  SSHConnection,
  type SSHConnectionRaw,
} from "../sshConnection/sshConnection.ts";
import {
  S3Connection,
  type S3ConnectionRaw,
} from "../s3Connection/s3Connection.ts";
import {
  DatabaseConnection,
  type DatabaseConnectionRaw,
} from "../databaseConnection/databaseConnection.ts";

export type ConfigRaw = {
  id?: number | undefined;
  name?: string;
  key?: string;
  ssh_connection?: SSHConnectionRaw | null;
  s3_connection?: S3ConnectionRaw | null;
  database_connection?: DatabaseConnectionRaw | null;
  max_versions?: number
  auto_build?: boolean
};

export class Config implements BaseModel {
  id: number | undefined;
  name: string;
  key: string;
  sshConnection: SSHConnection | null;
  s3Connection: S3Connection | null;
  databaseConnection: DatabaseConnection;
  autoBuild: boolean
  maxVersions: number

  constructor(raw: ConfigRaw) {
    this.id = raw.id;
    this.name = raw.name || "";
    this.sshConnection = raw.ssh_connection
      ? new SSHConnection(raw.ssh_connection)
      : null;
    this.s3Connection = raw.s3_connection
      ? new S3Connection(raw.s3_connection)
      : null;
    this.key = raw.key || "";
    this.databaseConnection = new DatabaseConnection(
      raw.database_connection || {}
    );
    this.maxVersions = raw.max_versions || 3
    this.autoBuild = raw.auto_build || false
  }

  toJson(): Record<string, any> {
    return {
      name: this.name || null,
      key: this.key || null,
      max_versions: this.maxVersions,
      ssh_connection: this.sshConnection?.id || null,
      s3_connection: this.s3Connection?.id || null,
      database_connection: this.databaseConnection.toJson(),
      auto_build: this.autoBuild
    };
  }
}
