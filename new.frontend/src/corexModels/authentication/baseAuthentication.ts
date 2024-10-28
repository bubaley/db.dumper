import moment from 'moment'
import {
  BaseAuthenticationUser,
  type BaseAuthenticationUserRaw,
} from './baseAuthenticationUser'
import { reactive } from 'vue'
import {
  BaseAuthenticationTokens,
  type TokensRaw,
} from '@/corexModels/authentication/baseAuthenticationTokens'
import type { AxiosResponse } from 'axios'
import { api } from '@/boot/axios'

export class BaseAuthentication {
  user: BaseAuthenticationUser | null = null
  tokens: BaseAuthenticationTokens

  tokensClass = BaseAuthenticationTokens
  userClass = BaseAuthenticationUser

  settings = {
    urls: {
      login: 'token/',
      me: '/users/me/',
      register: '/users/',
      refresh: '/token/refresh/',
      changePassword: '/users/change_password/',
    },
    apiHeader: {
      key: 'Authorization',
      type: 'Bearer',
    },
  }

  constructor() {
    this.tokens = this.tokensClass.getFromStorage()
    this.setApiHeader()
  }

  async me() {
    if (!this.tokens.accessIsValid) throw Error('Access token is not valid.')
    this.user = await this._loadUser()
    return this.user
  }

  async refresh(): Promise<void> {
    const result: AxiosResponse<TokensRaw> = await api.post(
      this.settings.urls.refresh,
      { refresh: this.tokens.refresh },
    )
    this.tokens = new this.tokensClass(result.data.access, result.data.refresh)
    this.setApiHeader()
  }

  async login(data: unknown) {
    this.logout()
    try {
      const response: AxiosResponse<TokensRaw> = await api.post(
        this.settings.urls.login,
        data,
      )
      this.tokens = new this.tokensClass(
        response.data.access,
        response.data.refresh,
      )
      this.setApiHeader()
      this.user = await this._loadUser()
      return {
        user: this.user,
        tokens: this.tokens,
      }
    } catch {
      throw Error('Fail login')
    }
  }

  async register(data: unknown) {
    this.logout()
    try {
      await api.post(this.settings.urls.register, data)
      return await this.login(data)
    } catch {
      throw Error('Register fail')
    }
  }

  async changePassword(data: unknown) {
    try {
      return await api.post(this.settings.urls.changePassword, data)
    } catch {
      throw Error('Change password fail')
    }
  }

  logout(): void {
    this.user = null
    this.tokens.removeTokens()
    Object.assign(api.defaults.headers, { Authorization: null })
  }

  setApiHeader(): void {
    const apiHeader = this.settings.apiHeader
    if (!this.tokens.access) return
    Object.assign(api.defaults.headers, {
      [apiHeader.key]: apiHeader.type
        ? `${apiHeader.type} ${this.tokens.access}`
        : this.tokens.access,
    })
  }

  async validateTokens(): Promise<void> {
    let shouldRefresh = false
    if (this.tokens.access) {
      const date = this.tokens.getJwtData(this.tokens.access).date
      if (moment.utc().add('1', 'day') >= date) {
        shouldRefresh = true
      }
    } else shouldRefresh = true
    if (shouldRefresh && this.tokens.refreshIsValid) {
      await this.refresh()
    }
  }

  private async _loadUser(): Promise<BaseAuthenticationUser> {
    try {
      const response: AxiosResponse<BaseAuthenticationUserRaw> = await api.get(
        this.settings.urls.me,
      )
      return new this.userClass(response.data)
    } catch {
      throw Error('Fail with load user.')
    }
  }
}

export const auth = reactive(new BaseAuthentication())
