import type { ILoginCredentials } from "@/types/auth/ILoginCredentials";

export class LoginCredentials implements ILoginCredentials {
    constructor(
        public emailOrUsername: string,
        public password: string,
        public rememberMe: boolean
    ) {}
}