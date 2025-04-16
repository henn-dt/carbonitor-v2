// src/services/IProductSnapshotService.ts
import type { IProduct } from '@/types/product/IProduct';
import type { EPD } from 'lcax';

export interface IProductSnapshotService {
  getProductSnapshotbyEpd(epd : EPD) : IProduct | null
  convertEpdToProduct(epd : EPD) : Promise<IProduct>
}