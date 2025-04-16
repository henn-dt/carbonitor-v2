import type { Permission } from "@/types/permissions/PermissionEnum";
import type { IAuthUser } from "@/types/auth/IAuthUser";

export interface IAuthState {
    user: IAuthUser | null;
    accessToken: string | null;
    refreshToken: string | null;
    permissions: Permission[] | null;
    authenticated: boolean;
    isRefreshing: boolean;
    rememberMe: boolean;
    accessTokenExpires: Date | null;
    refreshTokenExpires: Date | null;
}