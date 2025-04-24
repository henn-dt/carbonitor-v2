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
			:singleSelection="singleSelection"
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
	props: {
	    // If single selection mode (selecting one deselects the previous)
	    singleSelection: {
	      type: Boolean,
	      default: false
	    },
	    // Optionally provide initial selection(s)
	    selected: {
	      type: Array as () => ColumnDefinition[],
	      default: undefined
	    }
	  },
	emits: ['columnsChanged'],
	setup(props, { emit }) {
		// State
		const showColumnSelector = ref(false);

    	// Use the selected prop for initial value if provided
    	const initialSelected = props.selected && props.selected.length
    	  ? props.selected
    	  : getDefaultMoreImpactCategoryColumns();

    	// Separate for fixed and "more" columns
    	// If "selected" contains fixed category keys: distribute accordingly
    	const inFixed = (c: ColumnDefinition) => fixedImpactCategories.some(fc => fc.key === c.key);

    	const initialFixed = initialSelected.filter(inFixed);
    	const initialMore = initialSelected.filter(c => !inFixed(c));

    	// State for selected columns
    	const selectedColumns = ref<ColumnDefinition[]>(initialMore);
    	const activeFixedCategories = ref<ColumnDefinition[]>(initialFixed.length > 0
    	  ? initialFixed
    	  : fixedImpactCategories.filter(category => category.default)
    	);

		// Methods
		const isActive = (category: ColumnDefinition) => activeFixedCategories.value.some(cat => cat.key === category.key);

		const toggleCategory = (category: ColumnDefinition) => {
    	  if (props.singleSelection) {
    	    // Single selection: only one fixed can be active at a time
    	    if (!isActive(category)) {
    	      activeFixedCategories.value = [category];
    	      selectedColumns.value = []; // Optionally, clear more columns in single mode
    	    }
    	    // else do nothing (no deselection in single mode)
    	  } else {
    	    // Multi-select: behave as before
    	    if (isActive(category)) {
    	      activeFixedCategories.value = activeFixedCategories.value.filter(cat => cat.key !== category.key);
    	    } else {
    	      activeFixedCategories.value.push(category);
    	    }
    	  }
    	  emitCombinedCategories();
    	};

    	const updateImpactColumns = (columns: ColumnDefinition[]) => {
    	  if (props.singleSelection && columns.length > 0) {
    	    // Only keep the last selected
    	    selectedColumns.value = [columns[columns.length - 1]];
    	    // And force fixed none (optional: clear fixed when "other" selected)
    	    activeFixedCategories.value = [];
    	  } else {
    	    selectedColumns.value = columns;
    	  }
    	  emitCombinedCategories();
    	};

		const emitCombinedCategories = () => emit('columnsChanged', [...activeFixedCategories.value, ...selectedColumns.value]);

		return {
			moreImpactOptions: moreImpactCategoryColumns,
			selectedColumns,
			showColumnSelector,
			fixedImpactCategories,
			isActive,
			toggleCategory,
			updateImpactColumns,
			singleSelection: props.singleSelection
		};
	}
});
</script>

<style scoped>

</style>