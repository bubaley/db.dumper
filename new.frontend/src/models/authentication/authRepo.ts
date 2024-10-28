import { reactive } from 'vue';
import { Authentication } from './auth';
import { authenticationApi } from './authApi';
import { authentication } from './authentication';
import BaseRepo from '@/corexModels/apiModels/baseRepo'

export class AuthenticationRepo extends BaseRepo<Authentication> {
  api = authenticationApi;

  async initialise() {
    await authentication.validateTokens();
    await authentication.me();
  }


}

export const authRepo = reactive(new AuthenticationRepo());
