import type { Permission } from "@/types/permissions/PermissionEnum";
import type { IAuthTokens } from "@/types/auth/IAuthTokens";

export interface IAuthResponse extends IAuthTokens {
    user_id: number;
    username: string;
    email: string;
    permissions: Permission[];
}