import type { IAuthUser } from "@/types/auth/IAuthUser";
import type { Permission } from "../permissions/PermissionEnum";

export interface IStorage {
    access_token?: string | null;
    refresh_token?: string | null;
    access_token_expires?: string | null;
    refresh_token_expires?: string | null;
    user?: IAuthUser | null;
    permissions?: Permission[] | null;
}