

export interface IMappedEntity<T> {
    entity: T
    quantity: number
    elementMapId: string
}

export interface IMappedEntities<T>{
    [mapping_id : string]: IMappedEntity<T>[] 
}