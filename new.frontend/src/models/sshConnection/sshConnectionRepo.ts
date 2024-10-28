import BaseRepo from '@/corexModels/apiModels/baseRepo'
import { sshConnectionApi } from '@/models/sshConnection/sshConnectionApi'
import type { SSHConnection } from '@/models/sshConnection/sshConnection'
import { reactive } from 'vue'

export class SSHConnectionRepo extends BaseRepo<SSHConnection> {
    api = sshConnectionApi
}

export const sshConnectionRepo = reactive(new SSHConnectionRepo())
