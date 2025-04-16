import type { IUser } from "@/types/user/IUser";

// src/types/user/IUserDetail.ts
export interface IUserDetail extends IUser {
    is_verified: boolean;
    is_active: boolean;
    auth_method: string;
    last_login_at: string;
    created_at: string;
    updated_at: string;
}