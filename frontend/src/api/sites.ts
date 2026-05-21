import { apiClient } from './client';

export interface Site {
  id: number;
  name: string;
  domain: string;
  api_key: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SiteCreatePayload {
  name: string;
  domain: string;
}

export interface PaginatedResponse<T> {
  count: number;
  page: number;
  page_size: number;
  total_pages: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export const sitesApi = {
  list: () => apiClient.get<PaginatedResponse<Site>>('/sites/').then((r) => r.data),

  get: (id: number) => apiClient.get<Site>(`/sites/${id}/`).then((r) => r.data),

  create: (payload: SiteCreatePayload) =>
    apiClient.post<Site>('/sites/', payload).then((r) => r.data),

  update: (id: number, payload: Partial<SiteCreatePayload> & { is_active?: boolean }) =>
    apiClient.patch<Site>(`/sites/${id}/`, payload).then((r) => r.data),

  remove: (id: number) => apiClient.delete(`/sites/${id}/`),

  regenerateApiKey: (id: number) =>
    apiClient
      .post<{ api_key: string }>(`/sites/${id}/regenerate-api-key/`)
      .then((r) => r.data),
};
