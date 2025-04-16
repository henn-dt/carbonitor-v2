import type { IAuthUser } from '@/types/auth/IAuthUser';

export class AuthUser implements IAuthUser {
    constructor(
        public id: number,
        public email?: string,
        public username?: string
    ) {}
}