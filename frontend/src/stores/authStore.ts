import { defineStore } from 'pinia';
import { AuthState } from '@/types/auth/AuthState';
import type { IAuthState } from '@/types/auth/IAuthState';
import type { IAuthUser } from '@/types/auth/IAuthUser';
import type { Permission } from '@/types/permissions/PermissionEnum';

export const useAuthStore = defineStore('auth', {
  state: (): IAuthState => ({
    user: null,
    accessToken: null,
    refreshToken: null,
    permissions: null,
    authenticated: false,
    isRefreshing: false,
    rememberMe: false,
    accessTokenExpires: null,
    refreshTokenExpires: null,
  }),

  getters: {
    isLoggedIn: (state) => state.authenticated,
    getAccessToken: (state) => state.accessToken,
    getRefreshToken: (state) => state.refreshToken,
    getUser: (state) => state.user,
    getPermissions: (state) => state.permissions,
    isRememberMe: (state) => state.rememberMe,
    isAccessTokenExpired: (state) => state.accessTokenExpires ? new Date() > state.accessTokenExpires : true,
    isRefreshTokenExpired: (state) => state.refreshTokenExpires ? new Date() > state.refreshTokenExpires : true,
  },

  actions: {
    setUser(user: IAuthUser | null): void {
      this.user = user;
    },
    
    setAccessToken(accessToken: string): void {
      this.accessToken = accessToken;
    },

    setRefreshToken(refreshToken: string): void {
      this.refreshToken = refreshToken;
    },

    setPermissions(permissions: Permission[]): void {
      this.permissions = permissions;
    },

    setAuthenticated(isAuthenticated: boolean): void {
      this.authenticated = isAuthenticated;
    },

    setRememberMe(rememberMe: boolean): void {
      this.rememberMe = rememberMe;
    },

    setAccessTokenExpiry(expiryDate: Date | null): void {
      this.accessTokenExpires = expiryDate;
    },

    setRefreshTokenExpiry(expiryDate: Date | null): void {
      this.refreshTokenExpires = expiryDate;
    },

    logout(): void {
      this.updateAuthenticationData({
        user: null,
        accessToken: null,
        refreshToken: null,
        permissions: null,
        rememberMe: false,
        accessTokenExpires: null,
        refreshTokenExpires: null
      })
      this.setAuthenticated(false);
    },

    refreshAuthentication(accessToken: string, refreshToken: string, permissions: Permission[], rememberMe: boolean): void {
      this.setAccessToken(accessToken);
      this.setRefreshToken(refreshToken);
      this.setPermissions(permissions);
      this.setRememberMe(rememberMe);
      this.setAuthenticated(true);
    },

    updateAuthenticationData({
      user,
      accessToken,
      refreshToken,
      permissions,
      rememberMe,
      accessTokenExpires,
      refreshTokenExpires
    }: any): void {
      this.setUser(user);
      this.setAccessToken(accessToken);
      this.setRefreshToken(refreshToken);
      this.setPermissions(permissions);
      this.setRememberMe(rememberMe);
      this.setAccessTokenExpiry(accessTokenExpires);
      this.setRefreshTokenExpiry(refreshTokenExpires);
    }
  }
});