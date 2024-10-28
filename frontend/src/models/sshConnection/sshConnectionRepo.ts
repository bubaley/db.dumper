import {SSHConnection} from './sshConnection.ts'
import {reactive} from 'vue'
import BaseRepo from "../../corexModels/apiModels/baseRepo.ts";
import {sshConnectionApi} from "./sshConnectionApi.ts";

export class SSHConnectionRepo extends BaseRepo<SSHConnection> {
    api = sshConnectionApi
}

export const sshConnectionRepo = reactive(new SSHConnectionRepo())
