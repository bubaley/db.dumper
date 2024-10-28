import {SSHConnection, SSHConnectionRaw} from './sshConnection.ts';
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";


export class SSHConnectionApi extends BaseModelApi<SSHConnection> {
    routeName = 'ssh_connections'
    fromJson = (json: SSHConnectionRaw) => new SSHConnection(json)
}

export const sshConnectionApi = new SSHConnectionApi();
