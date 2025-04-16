import type { IAuthUser } from "@/types/auth/IAuthUser";
import type { Permission } from "../permissions/PermissionEnum";

export class AuthState {
    user: IAuthUser | null = null;
    accessToken: string | null = null;
    refreshToken: string | null = null;
    permissions: Permission[] | null = null;
    authenticated: boolean = false;
    isRefreshing: boolean = false;
    rememberMe: boolean = false;
    accessTokenExpires: Date | null = null;
    refreshTokenExpires: Date | null = null;
  
    constructor() {}

    setUser(user: IAuthUser | null): void {
        this.user = user;
    }

    setAccessToken(accessToken: string): void {
        this.accessToken = accessToken;
    }

    setRefreshToken(refreshToken: string): void {
        this.refreshToken = refreshToken;
    }

    setPermissions(permissions: Permission[] | null): void {
        this.permissions = permissions;
    }

    setAuthenticated(isAuthenticated: boolean): void {
        this.authenticated = isAuthenticated;
    }

    setRememberMe(rememberMe: boolean): void {
        this.rememberMe = rememberMe;
    }

    setAccessTokenExpiry(expiryDate: Date): void {
        this.accessTokenExpires = expiryDate;
    }

    setRefreshTokenExpiry(expiryDate: Date): void {
        this.refreshTokenExpires = expiryDate;
    }

    logout(): void {
        this.user = null;
        this.accessToken = null;
        this.refreshToken = null;
        this.permissions = null;
        this.authenticated = false;
        this.isRefreshing = false;
        this.rememberMe = false;
        this.accessTokenExpires = null;
        this.refreshTokenExpires = null;
    }
}