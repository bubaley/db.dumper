import axios from "axios";

// let baseURL = process.env.DEV ? "http://127.0.0.1:8000/api/v1" : "/api/v1";
// let baseURL = '/api/v1'
let baseURL = 'http://127.0.0.1:8000/api/v1'

// try {
//   if (process.env.BASE_URL) baseURL = process.env.BASE_URL;
// } catch {}
export const api = axios.create({ baseURL });
