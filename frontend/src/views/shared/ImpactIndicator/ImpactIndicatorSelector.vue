<template>
	<div class="selector-items-container">
		<a class="section-title">Indicators</a>
			
			<!-- Fixed impact categories -->
			<div 
				v-for="category in fixedImpactCategories" 
				:key="category.key"
				class="selector-item-tooltip-container">
				<div class="selector-item"
				:class="{ 'active': isActive(category) }"
				@click="toggleCategory(category)"
				>
					<span class="icon"
					:class="category.key"></span>
					<span class="text">{{ category.label }}</span>
				</div>
				<span class="tooltip">{{ category.tooltip }}</span>
			</div>
			<!-- More button -->
			<div class="selector-item-tooltip-container">
				<div 
					class="selector-item" 
					:class="{ 'active': showColumnSelector || selectedColumns.length > 0  }"
					@click="showColumnSelector = true"
				>
					<span class="icon more"></span>
					<span class="text">Other</span>
				</div>
				<span class="tooltip"> 
					{{ selectedColumns.length > 0 
           			? 'Selected indicators: ' + selectedColumns.map(col => col.label).join(', ')
           			: 'Select additional impact indicators' }}
					</span>
			</div>
		

		<!-- Column Selection Modal Component -->
		<ColumnSelector
			v-model="showColumnSelector"
			:items="moreImpactOptions"
			:selected="selectedColumns"
			@update="updateImpactColumns"
		>
			<template #header>
				<a class="section-title">More Indicators</a>
			</template>
		</ColumnSelector>
	</div>
</template>
    
<script lang="ts">
	import { defineComponent, ref, computed } from 'vue';
	import ColumnSelector from '@/views/shared/ColumnSelector/ColumnSelector.vue';
	import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
	import { fixedImpactCategories, moreImpactCategoryColumns, getDefaultMoreImpactCategoryColumns } from '@/views/shared/ImpactIndicator/ImpactIndicatorDefinitions';
  
export default defineComponent({
	name: 'ImpactIndicatorSelector',
	components: { ColumnSelector },
	emits: ['columnsChanged'],
	setup(_, { emit }) {
		// State
		const showColumnSelector = ref(false);
		const selectedColumns = ref<ColumnDefinition[]>(getDefaultMoreImpactCategoryColumns());
		const activeFixedCategories = ref<ColumnDefinition[]>( fixedImpactCategories.filter(category => category.default) );

		// Methods
		const isActive = (category: ColumnDefinition) => activeFixedCategories.value.some(cat => cat.key === category.key);

		const toggleCategory = (category: ColumnDefinition) => {
			if (isActive(category)) { activeFixedCategories.value = activeFixedCategories.value.filter(cat => cat.key !== category.key); }
			else { activeFixedCategories.value.push(category); }
			emitCombinedCategories();
		};

		const updateImpactColumns = (columns: ColumnDefinition[]) => { selectedColumns.value = columns; emitCombinedCategories(); };
		const emitCombinedCategories = () => emit('columnsChanged', [...activeFixedCategories.value, ...selectedColumns.value]);

		return {
			moreImpactOptions: moreImpactCategoryColumns,
			selectedColumns,
			showColumnSelector,
			fixedImpactCategories,
			isActive,
			toggleCategory,
			updateImpactColumns
		};
	}
});
</script>

<style scoped>

</style>