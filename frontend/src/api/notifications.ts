import { apiClient } from './client';

export type NotificationType = 'anomaly' | 'info' | 'warning' | 'success';

export interface Notification {
  id: number;
  type: NotificationType;
  title: string;
  message: string;
  site: number | null;
  site_name: string | null;
  is_read: boolean;
  created_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  results: T[];
}

export const notificationsApi = {
  list: (unreadOnly = false) =>
    apiClient
      .get<PaginatedResponse<Notification>>('/notifications/', {
        params: unreadOnly ? { unread_only: 'true' } : {},
      })
      .then((r) => r.data),

  unreadCount: () =>
    apiClient.get<{ count: number }>('/notifications/unread-count/').then((r) => r.data.count),

  markRead: (id: number) => apiClient.post(`/notifications/${id}/mark-read/`),

  markAllRead: () => apiClient.post('/notifications/mark-all-read/'),
};
