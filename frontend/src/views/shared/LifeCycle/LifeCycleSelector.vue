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
    	props: {
    	    singleReuse: {
    	        type: Boolean,   //turning on reuse will turn off everything else.
    	        default: false
    	    }
    	},
		emits: ['lifeCycleChanged'],
		setup(props, { emit }) {
			// State
			const selectedStages = ref<ColumnDefinition[]>(getDefaultLifeCycleStages());

			// Methods
			const isActive = (category: ColumnDefinition) => 
			selectedStages.value.some(cat => cat.key === category.key);

			const toggleCategory = (category: ColumnDefinition) => {
            const isReuse = category.key === 'Reuse';
            const wasActive = isActive(category);

            if (props.singleReuse) {
                if (isReuse) {
            		// Prevent removing the last active (Reuse)
            		if (selectedStages.value.length === 1 && selectedStages.value[0].key === 'Reuse' && wasActive) {
            		    return;
            		}
            		// Always select only "reuse" (unless already the sole active)
            		selectedStages.value = wasActive ? selectedStages.value : [category];
                } else {
                    // If "reuse" was selected, replace it
                    if (selectedStages.value.length === 1 && selectedStages.value[0].key === 'Reuse') {
                        selectedStages.value = [category];
                    } else {
                        // Toggle this non-reuse stage
                        if (wasActive) {
							// Prevent removing if this is the last active
							if (selectedStages.value.length === 1) return;
                            selectedStages.value = selectedStages.value.filter(stage => stage.key !== category.key);
                        } else {
                            selectedStages.value = [...selectedStages.value, category];
                        }
                    }
                }
            } else {
                // Default: classic multi-select
                if (wasActive) {
					// Prevent removing the last active
					if (selectedStages.value.length === 1) return;
                    selectedStages.value = selectedStages.value.filter(stage => stage.key !== category.key);
                } else {
                    selectedStages.value = [...selectedStages.value, category];
                }
            }

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