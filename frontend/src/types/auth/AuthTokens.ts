import type { IAuthTokens } from "@/types/auth/IAuthTokens";

export class AuthTokens implements IAuthTokens {
    constructor(
        public access_token: string,
        public refresh_token: string,
        public access_token_expires: string,
        public refresh_token_expires: string
    ) {}
}