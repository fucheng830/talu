import type { AxiosProgressEvent, AxiosResponse, GenericAbortSignal } from 'axios'
import request from './axios'
import { useUserStore } from '@/store'

export interface HttpOption {
  url: string
  data?: any
  method?: string
  headers?: any
  onDownloadProgress?: (progressEvent: AxiosProgressEvent) => void
  signal?: GenericAbortSignal
  beforeRequest?: () => void
  afterRequest?: () => void
}

export interface Response<T = any> {
  data: T
  message: string | null
  status: string | null
}

function http<T = any>(
  { url, data, method, headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
) {
  const userStore = useUserStore()
  const successHandler = (res: AxiosResponse<Response<T>>) => {
    if (res.data)
      return res.data

    if (res.data.status === 'Fail' && res.data.message === 'Token已过期') {
      userStore.removeToken()
      window.location.reload()
    }

    return Promise.reject(res)
  }

  const failHandler = (error: Response<Error>) => {
    afterRequest?.()
    // 检查是否有错误响应，以及响应中是否包含了详细信息
    if (error.response && error.response.data && error.response.data.detail) {
      // 如果有详细信息，则抛出包含该详细信息的错误
      throw new Error(error.response.data.detail);
    } else {
      // 如果没有详细信息，抛出一个通用的错误
      throw new Error(error.message || 'Error');
    }
  }

  beforeRequest?.()
  const defaultHeaders = userStore.$state.userInfo?.access_token
    ? { 'Content-Type': 'application/json', 'Authorization': `Bearer ${userStore.$state.userInfo?.access_token}` }
    : { 'Content-Type': 'application/json' }

  headers = headers || defaultHeaders

  method = method || 'GET'

  const params = Object.assign(typeof data === 'function' ? data() : data ?? {}, {})

  return method === 'GET'
    ? request.get(url, { params, signal, onDownloadProgress }).then(successHandler, failHandler)
    : request.post(url, params, { headers, signal, onDownloadProgress }).then(successHandler, failHandler)
}

export function get<T = any>(
  { url, data, method = 'GET', onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}

export function post<T = any>(
  { url, data, method = 'POST', headers, onDownloadProgress, signal, beforeRequest, afterRequest }: HttpOption,
): Promise<Response<T>> {
  return http<T>({
    url,
    method,
    data,
    headers,
    onDownloadProgress,
    signal,
    beforeRequest,
    afterRequest,
  })
}

export default post
