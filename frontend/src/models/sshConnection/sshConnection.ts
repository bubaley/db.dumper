import { type BaseModel } from "../../corexModels/apiModels/baseModel.ts";

export type SSHConnectionRaw = {
  id?: number | undefined;
  name?: string;
  host?: string;
  port?: number;
  username?: string;
  password?: string | null;
  private_key?: string;
  passphrase?: string;
};

export class SSHConnection implements BaseModel {
  id: number | undefined;
  name: string;
  host: string;
  port: number;
  password: string;
  username: string;
  privateKey: string;
  passphrase: string;

  constructor(raw: SSHConnectionRaw) {
    this.id = raw.id;
    this.name = raw.name || "";
    this.host = raw.host || "";
    this.username = raw.username || "";
    this.port = raw.port || 22;
    this.password = raw.password || "";
    this.privateKey = raw.private_key || "";
    this.passphrase = raw.passphrase || "";
  }

  toJson(): Record<string, any> {
    return {
      name: this.name,
      host: this.host,
      username: this.username,
      port: this.port,
      password: this.password || undefined,
      private_key: this.privateKey || undefined,
      passphrase: this.passphrase || undefined,
    };
  }
}
