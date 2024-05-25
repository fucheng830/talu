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


// 获取用户列表
export function getUsers() {
  return api.get('/users')
}

// 获取特定用户信息
export function getUser(id) {
  return api.get(`/users/${id}`)
}

// 创建新用户
export function createUser(userData) {
  return api.post('/users', userData)
}

// 更新特定用户信息
export function updateUser(id, userData) {
  return api.put(`/users/${id}`, userData)
}

// 删除特定用户
export function deleteUser(id) {
  return api.delete(`/users/${id}`)
}