import type { IMappedEntities, IMappedEntity } from "@/types/mapping/IMappedEntity";
import type { IProductMappingService } from "./IProductMappingService";
import type { IBuildup, ReferenceSourceForProduct } from '@/types/buildup/IBuildup';
import type { IProductService } from "./IProductService";
import type { IProduct } from "@/types/product/IProduct"; 
import { injectable, inject } from "inversify";
import type { EPD} from "lcax";
import type { IProductSnapshotService } from "./IProductSnapshotService";
import { TYPES } from "@/di/types";

@injectable()
export class ProductMappingService implements IProductMappingService{
    constructor(
      @inject(TYPES.ProductService) private productService: IProductService,
      @inject(TYPES.ProductSnapshotService) private productSnapshotService: IProductSnapshotService
    ) {}

    /**
     * Validates product results
     * @param mapping Dictionary of products ordered by their mapping id
     * @param results Dictionary of results likewise ordered by their mapping id
     * @returns Object with validation status and error message if any
     */
    public validate(mapping: Record<string, any>, results: Record<string,  any>): { valid: boolean; error?: string } {
        // Check if products and results are defined
        if (!mapping || !results) {
          return { valid: false, error: "Products or results are undefined" };
        }

      // Check each product key has a corresponding result
      for (const productId in mapping) {
        if (!results[productId]) {
          return { 
            valid: false, 
            error: `Product with ID ${productId} does not have a corresponding result` 
          };
        }

        // Check that the result has a quantity property
        if (results[productId].quantity === undefined) {
          return { 
            valid: false, 
            error: `Result for product ID ${productId} is missing a quantity property` 
          };
        }

        // Check that quantity is a number
        if (typeof results[productId].quantity !== 'number') {
          return { 
            valid: false, 
            error: `Quantity for product ID ${productId} is not a number` 
          };
        }
      }

      // Check for orphan results (results with no matching product)
      for (const resultId in results) {
        if (!mapping[resultId]) {
          return { 
            valid: false, 
            error: `Result with ID ${resultId} does not have a corresponding product` 
          };
        }
      }

      return { valid: true };
    }

    async mapToEPD(product: ReferenceSourceForProduct, quantity : number, mappingId : string): Promise<IMappedEntity<IProduct>> {

      //this needs to change, i actually need the products. I need a "epd to product" method somewhere reachable
      // Logic to convert reference to product
      const type = product.type
      let epd : EPD | null

      // Check the type property to determine how to get the product
      if (type === 'actual') {
        // Use the entire entity to create a product
        epd = product as EPD;
        if (epd === null) {
          throw new Error('could not parse epd from buildup actual product');
        }
        return {
            elementMapId: mappingId,
            entity: await this.productSnapshotService.convertEpdToProduct(epd),
            quantity
        }
        
      } else if (type === 'reference') {
        // Ensure referenceUri exists
        if (!product.uri) {
          throw new Error('Reference type entity must have a uri property');
        }

        // Get product from the URI using ProductStore
        const productResponse = await this.productService.getProductByUri(product.uri)
        if (productResponse === null) {
          throw new Error('Failed to parse EPD data');
        }
        return {
          elementMapId: mappingId,
          entity: productResponse,
          quantity
      };
      } else {
        
        throw new Error(`Unsupported entity type: ${type}. Expected 'actual' or 'reference'`);
      }
    }
    
    async mapProducts(mapping: Record<string, ReferenceSourceForProduct>, results: Record<string,  any>): Promise<IMappedEntities<IProduct>>{

      //first, validate the mapping
      const validation = this.validate(mapping, results)
      if (!validation.valid) {
        throw new Error(validation.error)
      }

      let mappedEntities : IMappedEntities<IProduct> = {};

      // Process each product and its corresponding result
      for (const productId in mapping) {

        const product : ReferenceSourceForProduct = mapping[productId];
        const type = product.type

        // get the element id, checking if it´s an actual product or a reference
        let elementId : string 
        if (type === 'actual') {         
          elementId = product.metaData.model_mapping_element_id
        } else if (type === 'reference') {
          if (product.overrides === null) {
            throw new Error('Product is missing overrides');
          }

          const metaDataRaw = product.overrides.meta_data 
          let metaDataObj: { model_mapping_element_id?: string };
          
          if (typeof metaDataRaw === 'string') {
            try {
              metaDataObj = JSON.parse(metaDataRaw);
            } catch (error) {
              console.error('Error parsing meta_data string:', metaDataRaw);
              throw new Error(`Failed to parse meta_data: ${error}`);
            }
          } else {
            // It's already an object
            metaDataObj = metaDataRaw as unknown as { model_mapping_element_id?: string };
          }
          
          if (!metaDataObj || !metaDataObj.model_mapping_element_id) {
            throw new Error('Product is missing model_mapping_element_id in meta_data');
          }
          
          elementId = metaDataObj.model_mapping_element_id;
        } else {         
          throw new Error(`Unsupported entity type: ${type}. Expected 'actual' or 'reference'`);
        }

        const result = results[productId];
        const quantity = result.quantity

        const mappedProducts = await this.mapToEPD(product, quantity, productId);

        if (!mappedEntities[elementId]) {
          mappedEntities[elementId] = [];
        }

        // Add the mapped entity to the result array
        mappedEntities[elementId].push(mappedProducts)
        };
        return mappedEntities;
      }

      async generateMappingFromBuildups(buildups : IBuildup[]) : Promise<(Map<IBuildup , IMappedEntities<IProduct>>)> {
        const mappingsMap = new Map<IBuildup, IMappedEntities<IProduct>>();
  
        for (const buildup of buildups) {
          if (buildup.results === null) {
            throw new Error('Buildup has no result values');
          }
          
          const mappedEntities = await this.mapProducts(buildup.products, buildup.results);
          mappingsMap.set(buildup, mappedEntities);
        }
        
        return mappingsMap;
      }
    }