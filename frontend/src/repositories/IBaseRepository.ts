export interface IBaseRepository {
    get<T>(url: string, params?: any): Promise<T>;
    post<T>(url: string, payload: any): Promise<T>;
    put<T>(url: string, payload: any): Promise<T>;
    delete<T>(url: string, params?: any): Promise<T>;
}