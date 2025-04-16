import type { Permission } from "@/types/permissions/PermissionEnum";
import type { IStorage } from "@/types/storage/IStorage";
import type { IAuthUser } from "@/types/auth/IAuthUser";

export interface IStorageService {
    // GETTERS
    getAccessToken(): string | null;
    getRefreshToken(): string | null;
    getAccessTokenExpiry(): string | null;
    getRefreshTokenExpiry(): string | null;
    getUser(): IAuthUser | null;
    getPermissions(): Permission[] | null;
    getAllStorageKeys(): IStorage;

    // SETTERS
    setAccessTokenExpiry(accessTokenExpires: string | null | undefined): void;
    setRefreshTokenExpiry(refreshTokenExpires: string | null | undefined): void;
    setAccessToken(accessToken: string | null | undefined): void;
    setRefreshToken(refreshToken: string | null | undefined): void;
    setUser(user: IAuthUser | null | undefined): void;
    setPermissions(permissions: Permission[] | null | undefined): void;
    setAllStorageKeys(storage: IStorage | undefined): void;

    // DELETE
    clear(): void;
}