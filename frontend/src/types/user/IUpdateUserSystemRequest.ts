// src/types/user/IUpdateUserSystemRequest.ts
export interface IUpdateUserSystemRequest {
    auth_method?: string;
    is_active?: boolean;
    is_verified?: boolean;
    last_login_at?: string;
}