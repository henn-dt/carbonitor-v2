<template>
    <div class="selector-items-container">
        <div class="selector-item-tooltip-container">
            <div class="selector-item"
                :class="{ 'active': showColumnSelector }"
                @click="showColumnSelector = true"
            >
            <span class="icon columns"></span>
            <span class="text">Data Fields</span>

            </div>
            <!-- Column Selection Modal Component -->
            <ColumnSelector
                v-model="showColumnSelector"
                :items="columnsArray"
                :selected="selectedColumns"
                @update="updateColumns"
            >
                <template #header>
                    <a class="section-title">Products Data Fields</a>
                </template>
            </ColumnSelector>
            <span class="tooltip">Customize Product Columns</span>
        </div>
    </div>
</template>
  
<script lang="ts">
    import { defineComponent, ref, computed } from 'vue';
    import ColumnSelector from '@/views/shared/ColumnSelector/ColumnSelector.vue';
    import { productColumns, getDefaultProductColumns } from '@/views/user/components/products/productColumn/ProductColumnDefinitions';
    import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

    export default defineComponent({
        name: 'ProductColumnSelector',
        components: {
            ColumnSelector
        },
        emits: ['columnsChanged'],
        setup(_, { emit }) {
            // Use imported product columns
            const showColumnSelector = ref(false);
            // Initialize with default columns
            const selectedColumns = ref<ColumnDefinition[]>(getDefaultProductColumns());
            // Use imported product columns directly
            const columnsArray = productColumns;

            // Methods
            const updateColumns = (columns: ColumnDefinition[]) => {
                selectedColumns.value = columns;
                emit('columnsChanged', columns);
            };
            
            return {
                showColumnSelector,
                selectedColumns,
                columnsArray,
                updateColumns
            };
        }
    });
</script>

<style scoped>
    .button {
        width: 100%;
        padding: var(--spacing-sm);
        border-radius: var(--rad);
        border: 1px solid var(--color-grey);
        background: var(--color-light);
    }
    .button:hover {
        background-color: var(--color-highlight);
        border-color: var(--color-grey);
        transition: transform var(--dur) ease;
    }
    .button--active {
        background-color: var(--color-active);
        color: var(--color-light);
        font-weight: bold;
        border: 0;
    }
</style>

