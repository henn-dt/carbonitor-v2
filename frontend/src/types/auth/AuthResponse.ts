import type { IAuthResponse } from "@/types/auth/IAuthResponse"
import type { Permission } from "@/types/permissions/PermissionEnum"

export class AuthResponse implements IAuthResponse {
    constructor(
        public access_token: string,
        public refresh_token: string,
        public access_token_expires: string,
        public refresh_token_expires: string,
        public user_id: number,
        public username: string,
        public email: string,
        public permissions: Permission[]
    ) {}
}