import {Config, ConfigRaw} from './config.ts';
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";


export class ConfigApi extends BaseModelApi<Config> {
    routeName = 'configs'
    fromJson = (json: ConfigRaw) => new Config(json)
}

export const configApi = new ConfigApi();
