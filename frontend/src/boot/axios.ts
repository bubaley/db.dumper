import axios from 'axios'

// export let baseURL = '/api/v1'
export let baseURL = 'http://127.0.0.1:8000/api/v1'
//
// if (process.env.DEV) {
//     baseURL = 'http://127.0.0.1:8000/api/v1'
// }
// try {
//     if (process.env.BASE_URL) baseURL = process.env.BASE_URL
// } catch {
// }
const api = axios.create({baseURL})

export {api}
