import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { API_URL, STORAGE_KEYS } from '@/lib/constants';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const access = localStorage.getItem(STORAGE_KEYS.ACCESS);
  if (access && config.headers) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

let isRefreshing = false;
let pendingQueue: Array<(token: string | null) => void> = [];

const flushQueue = (token: string | null) => {
  pendingQueue.forEach((cb) => cb(token));
  pendingQueue = [];
};

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as InternalAxiosRequestConfig & { _retry?: boolean };
    if (
      error.response?.status === 401 &&
      original &&
      !original._retry &&
      !original.url?.includes('/auth/login') &&
      !original.url?.includes('/auth/refresh')
    ) {
      const refresh = localStorage.getItem(STORAGE_KEYS.REFRESH);
      if (!refresh) return Promise.reject(error);

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pendingQueue.push((token) => {
            if (token && original.headers) {
              original.headers.Authorization = `Bearer ${token}`;
              resolve(apiClient(original));
            } else {
              reject(error);
            }
          });
        });
      }

      original._retry = true;
      isRefreshing = true;
      try {
        const { data } = await axios.post(`${API_URL}/auth/refresh/`, { refresh });
        localStorage.setItem(STORAGE_KEYS.ACCESS, data.access);
        if (data.refresh) localStorage.setItem(STORAGE_KEYS.REFRESH, data.refresh);
        flushQueue(data.access);
        if (original.headers) original.headers.Authorization = `Bearer ${data.access}`;
        return apiClient(original);
      } catch (refreshError) {
        flushQueue(null);
        localStorage.removeItem(STORAGE_KEYS.ACCESS);
        localStorage.removeItem(STORAGE_KEYS.REFRESH);
        window.location.href = '/login';
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);
