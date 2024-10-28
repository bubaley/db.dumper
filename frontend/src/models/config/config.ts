import {BaseModel} from "../../corexModels/apiModels/baseModel.ts";
import {SSHConnection, SSHConnectionRaw} from "../sshConnection/sshConnection.ts";
import {S3Connection, S3ConnectionRaw} from "../s3Connection/s3Connection.ts";

export type ConfigRaw = {
    id?: number | undefined
    name?: string
    key?: string
    ssh_connection?: SSHConnectionRaw | null
    s3_connection?: S3ConnectionRaw | null
}

export class Config implements BaseModel {
    id: number | undefined
    name: string
    key: string
    sshConnection: SSHConnection | null
    s3Connection: S3Connection | null


    constructor(raw: ConfigRaw) {

        this.id = raw.id
        this.name = raw.name || ''
        this.sshConnection = raw.ssh_connection ? new SSHConnection(raw.ssh_connection) : null
        this.s3Connection = raw.s3_connection ? new S3Connection(raw.s3_connection) : null
        this.key = raw.key || ''
    }

    toJson(): Record<string, any> {
        return {}
    }
}