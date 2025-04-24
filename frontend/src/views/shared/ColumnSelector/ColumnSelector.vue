<template>
	<Teleport to="body">
		<Transition name="fade">
			<div v-if="modelValue" class="columnselector-backdrop" @mousedown.self="$emit('update:modelValue', false)">
				<div class="selectors-container-vertical" ref="containerRef">
					<!-- Header with title -->
					<div class="columnselector-header">
						<slot name="header">
							<a class="section-title">Select Items</a>
						</slot>
					</div>
					<!-- Body with single-column item list -->
					<div class="columnselector-body">
						<slot name="body">
							<div class="selector-items-container">
								<div 
									v-for="item in items" 
									:key="item.key" 
									class="selector-item-tooltip-container">
										<div class="selector-item"
										:class="{ 'active': isSelected(item) }"
										@click="toggleItem(item)"
										>
										<span class="text">{{ item.label }}</span>
										</div>
									<span class="tooltip">{{ item.tooltip }}</span>
								</div>
							</div>
						</slot>
					</div>
					<!-- Footer with only reset button -->
					<div class="columnselector-footer">
						<slot name="footer">
							<button class="button button-info" @click="resetSelection">DEFAULT</button>
						</slot>
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script lang="ts">
import { defineComponent, ref, watch, type PropType, onBeforeUnmount } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export default defineComponent({
	name: 'ColumnSelector',
	props: {
		modelValue: {
			type: Boolean,
			required: true
		},
		items: {
			type: Array as PropType<ColumnDefinition[]>,
			required: true
		},
		selected: {
			type: Array as PropType<ColumnDefinition[]>,
			required: true
		},
        singleSelection: {
            type: Boolean,
            default: false             // <------ Add this for optional single-select
        }
	},
	emits: ['update', 'update:modelValue'],
	setup(props, { emit }) {
		// Local copy of selected items
		const localSelected = ref<ColumnDefinition[]>([...props.selected]);
		// Reference to the container element
		const containerRef = ref<HTMLElement | null>(null);
		// Handle keyboard events for accessibility
		const handleKeyDown = (event: KeyboardEvent) => {
			if (props.modelValue && event.key === 'Escape') { emit('update:modelValue', false); }
		};
		
		// Update local selected values when props change
		watch(() => props.selected, (newVal) => { localSelected.value = [...newVal]; });
		
		// Reset tracking when show prop changes
		watch(() => props.modelValue, (newVal) => {
			if (newVal) { localSelected.value = [...props.selected]; window.addEventListener('keydown', handleKeyDown);}
			else { window.removeEventListener('keydown', handleKeyDown); }
		});
		
		// Check if an item is selected
		const isSelected = (item: ColumnDefinition): boolean => { return localSelected.value.some(selectedItem => selectedItem.key === item.key); };
		
		// Toggle item selection
        // --- changed implementation here if singleSelection is on! ---
        const toggleItem = (item: ColumnDefinition) => {
            if (props.singleSelection) {
                // select only one item at a time
                localSelected.value = [item];
            } else {
                const index = localSelected.value.findIndex(selectedItem => selectedItem.key === item.key);
                if (index === -1) {
                    localSelected.value.push(item);
                } else {
                    localSelected.value.splice(index, 1);
                }
            }
            emit('update', localSelected.value);
        };
		
		// Reset to default items
		const resetSelection = () => {
			localSelected.value = props.items.filter(item => item.default);
			emit('update', localSelected.value);
		};
		
		// Clean up event listeners
		onBeforeUnmount(() => {
			window.removeEventListener('keydown', handleKeyDown);
		});
		
		return {
			containerRef,
			localSelected,
			isSelected,
			toggleItem,
			resetSelection
		};
	}
});
</script>

<style scoped>
	/* Backdrop overlay */
	.columnselector-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		justify-content: flex-end;
		align-items: stretch;
		z-index: 1000;
		padding: var(--spacing-md);
	}

	/* Container */


	/* Button styles */
	.button {
		padding: var(--spacing-sm);
		border: 0;
		border-radius: var(--rad);
		font-weight: bold;
		cursor: pointer;
		transition: background-color 0.2s, opacity 0.2s;
		width: 100%;
	}
	
	.button-info {
		background-color: var(--color-light);
		color: var(--color-active);
	}
	.button-info:hover {
		background-color: var(--color-highlight);
	}

	/* Transition effects */
	.fade-enter-active,
	.fade-leave-active {
		transition: opacity 0.2s ease;
	}
	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}
</style>