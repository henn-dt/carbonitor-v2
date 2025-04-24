import type { IMappedEntities, IMappedEntity } from "@/types/mapping/IMappedEntity";
import type { IBuildup, ReferenceSourceForProduct } from "@/types/buildup/IBuildup";
import type { IProduct } from "@/types/product/IProduct";

export interface IProductMappingService {
    validate(mapping: Record<string, any>, results: Record<string,  any>): { valid: boolean; error?: string }
    mapToEPD(product: ReferenceSourceForProduct, quantity : number, mappingId : string): Promise<IMappedEntity<IProduct>>;
    mapProducts(mapping: Record<string, ReferenceSourceForProduct>, results: Record<string,  any>): Promise<IMappedEntities<IProduct>>;
    generateMappingFromBuildups(buildups : IBuildup[]) : Promise<(Map<IBuildup , IMappedEntities<IProduct>>)>;
}

