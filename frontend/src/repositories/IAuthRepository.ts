import type { IBaseRepository } from '@/repositories/IBaseRepository';
import type { IAuthResponse } from '@/types/auth/IAuthResponse';
import type { ILoginCredentials } from '@/types/auth/ILoginCredentials';
import type { IRegisterCredentials } from '@/types/auth/IRegisterCredentials';

export interface IAuthRepository extends IBaseRepository {
    login(credentials: ILoginCredentials): Promise<IAuthResponse>;
    register(credentials: IRegisterCredentials): Promise<IAuthResponse>;
    refresh(refreshToken: string): Promise<IAuthResponse>;
    logout(userId: number): Promise<void>;
}