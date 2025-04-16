

export interface IMappedEntity<T> {
    entity: T
    quantity: number
}

export interface IMappedEntities<T>{
    [mapping_id : string]: IMappedEntity<T>[] 
}