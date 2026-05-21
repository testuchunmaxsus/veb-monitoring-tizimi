import { apiClient } from './client';

export interface User {
  id: number;
  email: string;
  full_name: string;
  date_joined: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export interface RegisterPayload {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface LoginResponse extends AuthTokens {
  user: User;
}

export const authApi = {
  login: (payload: LoginPayload) =>
    apiClient.post<LoginResponse>('/auth/login/', payload).then((r) => r.data),

  register: (payload: RegisterPayload) =>
    apiClient.post<{ user: User; tokens: AuthTokens }>('/auth/register/', payload).then((r) => r.data),

  me: () => apiClient.get<User>('/auth/me/').then((r) => r.data),

  logout: (refresh: string) => apiClient.post('/auth/logout/', { refresh }),
};
