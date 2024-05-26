import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_GLOB_API_URL,
})

// 请求拦截器
api.interceptors.request.use((config) => {
  const token = useAuthStore().token
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    if (response.status === 200) return response.data
    throw new Error(response.status.toString())
  },
  (error) => {
    return Promise.reject(error)
  }
)


