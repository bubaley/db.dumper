import { Authentication, type AuthenticationRaw } from './auth'
import {BaseModelApi} from "../../corexModels/apiModels/baseModelApi.ts";

export class AuthenticationApi extends BaseModelApi<Authentication> {
  routeName = 'users'
  fromJson = (json: AuthenticationRaw) => new Authentication(json)
}

export const authenticationApi = new AuthenticationApi()
