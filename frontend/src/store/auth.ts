import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authApi, User, LoginPayload, RegisterPayload } from '@/api/auth';
import { STORAGE_KEYS } from '@/lib/constants';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (payload: LoginPayload) => Promise<void>;
  register: (payload: RegisterPayload) => Promise<void>;
  logout: () => Promise<void>;
  loadProfile: () => Promise<void>;
}

export const useAuth = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,

      login: async (payload) => {
        set({ isLoading: true });
        try {
          const data = await authApi.login(payload);
          localStorage.setItem(STORAGE_KEYS.ACCESS, data.access);
          localStorage.setItem(STORAGE_KEYS.REFRESH, data.refresh);
          set({ user: data.user, isAuthenticated: true, isLoading: false });
        } catch (e) {
          set({ isLoading: false });
          throw e;
        }
      },

      register: async (payload) => {
        set({ isLoading: true });
        try {
          const data = await authApi.register(payload);
          localStorage.setItem(STORAGE_KEYS.ACCESS, data.tokens.access);
          localStorage.setItem(STORAGE_KEYS.REFRESH, data.tokens.refresh);
          set({ user: data.user, isAuthenticated: true, isLoading: false });
        } catch (e) {
          set({ isLoading: false });
          throw e;
        }
      },

      logout: async () => {
        const refresh = localStorage.getItem(STORAGE_KEYS.REFRESH);
        if (refresh) {
          try {
            await authApi.logout(refresh);
          } catch { /* server xato qilsa ham token tozalanadi */ }
        }
        localStorage.removeItem(STORAGE_KEYS.ACCESS);
        localStorage.removeItem(STORAGE_KEYS.REFRESH);
        set({ user: null, isAuthenticated: false });
      },

      loadProfile: async () => {
        const access = localStorage.getItem(STORAGE_KEYS.ACCESS);
        if (!access) return;
        try {
          const user = await authApi.me();
          set({ user, isAuthenticated: true });
        } catch {
          set({ user: null, isAuthenticated: false });
        }
      },
    }),
    {
      name: 'vmt-auth',
      partialize: (state) => ({ user: state.user, isAuthenticated: state.isAuthenticated }),
    }
  )
);
