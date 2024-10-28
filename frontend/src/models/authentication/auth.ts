import { BaseModel } from 'src/corexModels/apiModels/baseModel'

export type AuthenticationRaw = {
  id: number | string | undefined
}

export class Authentication implements BaseModel {
  id: number | string | undefined

  constructor(raw: AuthenticationRaw) {
    this.id = raw.id
  }

  toJson(): Record<string, any> {
    return {
      id: this.id,
    }
  }
}
