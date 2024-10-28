import { BaseModelApi } from '@/corexModels/apiModels/baseModelApi'
import { Config, type ConfigRaw } from '@/models/config/config'


export class ConfigApi extends BaseModelApi<Config> {
    routeName = 'configs'
    fromJson = (json: ConfigRaw) => new Config(json)
}

export const configApi = new ConfigApi();
