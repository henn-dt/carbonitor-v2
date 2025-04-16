// frontend/src/types/modal/IModal.ts

import type { BuildupDetailParams } from "./BuildupModal";
import type { CategoryDetailParams } from "./CategoryModal";

// export type ModalName = 'product-detail' | 'buildup-detail' | 'category-detail' |
//                        'select-product' | 'select-buildup' | 'select-category' // etc

export type ModalName =  'buildup-detail' | 'category-detail' 

export type ModalParams =
    | { name: 'buildup-detail'; params: BuildupDetailParams }
    | { name: 'category-detail'; params: CategoryDetailParams }
// add more as needed
        

export type ModalEntry = ModalParams;