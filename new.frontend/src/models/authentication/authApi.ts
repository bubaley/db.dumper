import { BaseModelApi } from '@/corexModels/apiModels/baseModelApi'
import { Authentication, type AuthenticationRaw } from '@/models/authentication/auth'

export class AuthenticationApi extends BaseModelApi<Authentication> {
  routeName = 'users'
  fromJson = (json: AuthenticationRaw) => new Authentication(json)
}

export const authenticationApi = new AuthenticationApi()
