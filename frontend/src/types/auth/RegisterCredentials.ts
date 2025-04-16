import type { IRegisterCredentials } from "@/types/auth/IRegisterCredentials";

export class RegisterCredentials implements IRegisterCredentials {
    constructor(
        public email: string,
        public username: string,
        public password: string,
        public confirm_password: string
    ) {}
}