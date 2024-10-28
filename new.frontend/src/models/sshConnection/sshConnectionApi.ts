import { BaseModelApi } from '@/corexModels/apiModels/baseModelApi'
import { SSHConnection, type SSHConnectionRaw } from '@/models/sshConnection/sshConnection'


export class SSHConnectionApi extends BaseModelApi<SSHConnection> {
    routeName = 'ssh_connections'
    fromJson = (json: SSHConnectionRaw) => new SSHConnection(json)
}

export const sshConnectionApi = new SSHConnectionApi();
