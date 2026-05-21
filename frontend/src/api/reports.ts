import { apiClient } from './client';

export interface Report {
  id: number;
  site: number;
  site_name: string;
  format: 'pdf' | 'csv';
  status: 'pending' | 'processing' | 'done' | 'failed';
  date_from: string;
  date_to: string;
  file_url: string | null;
  error_message: string;
  created_at: string;
  completed_at: string | null;
}

export interface ReportCreatePayload {
  site: number;
  format: 'pdf' | 'csv';
  date_from: string;
  date_to: string;
}

export interface PaginatedResponse<T> {
  count: number;
  results: T[];
}

export const reportsApi = {
  list: () => apiClient.get<PaginatedResponse<Report>>('/reports/').then((r) => r.data),

  create: (payload: ReportCreatePayload) =>
    apiClient.post<Report>('/reports/', payload).then((r) => r.data),

  download: (id: number) =>
    apiClient
      .get(`/reports/${id}/download/`, { responseType: 'blob' })
      .then((r) => r.data as Blob),
};
