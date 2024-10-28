import { reactive } from 'vue'
import {BaseAuthentication} from "../../corexModels/authentication/baseAuthentication.ts";

export class Authentication extends BaseAuthentication {}
export const authentication = reactive(new Authentication())
