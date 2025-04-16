<template>
	<div class="selector-items-container">
		<a class="section-title">Life Cycle Stage</a>

			<div 
				v-for="category in lifeCycleStages" 
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

	</div>
</template>

<script lang="ts">
	import { defineComponent, ref } from 'vue';
	import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
	import { lifeCycleStages, getDefaultLifeCycleStages } from '@/views/shared/LifeCycle/LifeCycleDefinitons';

	export default defineComponent({
		name: 'LifeCycleSelector',
		emits: ['lifeCycleChanged'],
		setup(_, { emit }) {
			// State
			const selectedStages = ref<ColumnDefinition[]>(getDefaultLifeCycleStages());

			// Methods
			const isActive = (category: ColumnDefinition) => 
			selectedStages.value.some(cat => cat.key === category.key);

			const toggleCategory = (category: ColumnDefinition) => {
				if (isActive(category)) { selectedStages.value = selectedStages.value.filter(stage => stage.key !== category.key);}
				else { selectedStages.value = [...selectedStages.value, category]; }
				emit('lifeCycleChanged', selectedStages.value);
			};

			return {
				selectedStages,
				lifeCycleStages,
				isActive,
				toggleCategory
			};
		}
	});
</script>