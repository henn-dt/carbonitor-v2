<template v-if="!loading && !error">
    <!-- First group by classification system -->
    <div 
      v-for="(systemGroup, system) in groupedDisplayBuildups" 
      :key="system" 
      class="section-container" 
      :id="`${system.toLowerCase()}Section`"
    >
    <div class="filter-item" @click="toggleSection(`${system.toLowerCase()}Section`)">
      <div class="section-title" >
        {{ system }}
      </div>
      <span class="icon chevron collapse-up"></span>
    </div>
      
      <div class="filter-groups-container">
        <!-- Then group by code+name combination within each system -->
        <div 
          v-for="(codeGroup, codeKey) in systemGroup" 
          :key="codeKey" 
          class="code-group"
          :id="`${codeKey.toLowerCase()}Buildups`"
        > <div class="filter-item">
            <input type="checkbox"
                :class="{ 'partial': isCodeGroupPartiallySelected(codeKey) }"
                :checked="isCodeGroupSelected(codeKey)"
                @click.stop="toggleCodeGroup(codeKey, codeGroup)"
                >
            <div class="group-title" @click="toggleBuildups(`${codeKey.toLowerCase()}Buildups`, codeKey)">
                <div class = "label">
                    <span class="code">{{ codeKey.split('|')[0] }}</span>
                    <span> | </span>
                    <span class="name">{{ codeKey.split('|')[1] }}</span>
                </div>
                <span class="icon chevron" :class="expandedCodeGroups.has(codeKey) ? 'collapse-down' : 'collapse-up'"></span>
            </div>
            
          </div>
          
          <!-- List individual buildups within each code group -->
          <div class="filter-items-container"
          :style="{display: expandedCodeGroups.has(codeKey) ? 'block' : 'none'}"
          >
            <div 
              v-for="buildup in codeGroup" 
              :key="buildup.id" 
              class="buildup-item"             
            >   <div class="filter-item" @click="selectBuildup(buildup)">
                    <input type="checkbox"
                        
                        :checked="isBuildupSelected(buildup)"
                        @click.stop="selectBuildup(buildup)"
                        >
                    <span class="text" 
                      @click="selectBuildup(buildup)"
                      :class="{'not-in-filter': isBuildupSelectedButNotInFilter(buildup)}">
                        {{ buildup.name }}
                    </span>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>


<script lang="ts">
import { defineComponent, ref, computed, watch, onMounted } from 'vue';
import type { IBuildup } from '@/types/buildup/IBuildup';

export default defineComponent({
  name: 'BuildupList',
  props: {
    buildups: {
      type: Array as () => IBuildup[],
      required: true
    },
    loading : { 
      type: Boolean, 
      required: true},
    error : { 
      type: String , 
      required: false},
    filteredBuildups : {
      type: Array as () => number[],       
      required: false,
      default: () => []}
      ,
    selectedBuildups : {
      type: Array as () => number[],       
      required: false,
      default: () => []}
  },
  emits: ['update:selectedBuildups'],
  setup(props, {emit }) {

    const selectedBuildup = ref<IBuildup | null>(null);
    const expandedCodeGroups = ref<Set<string>>(new Set());
    

    // State for tracking selected buildups
    const selectedBuildupIds = ref<Set<string | number>>(new Set());
    const selectedCodeGroups = ref<Set<string>>(new Set());

    // Initialize selected buildups from props
    onMounted(() => {
      selectedBuildupIds.value.clear();
      selectedCodeGroups.value.clear();
      // Initialize with any existing filtered buildups (which are now indices)
      if (props.selectedBuildups.length > 0) {
        console.log('initial selected buildups')
        console.log(props.selectedBuildups)
        props.selectedBuildups.forEach(index => {
          if (props.buildups[index]) {
            selectedBuildupIds.value.add(props.buildups[index].id);
          }
        });
        updateCodeGroupSelections();
      }
    });

      // Computed property to determine which buildups to display
      const displayBuildups = computed(() => {
        const displaySet = new Set<IBuildup>();
      
      // First, add all buildups that match the current filter
      if (props.filteredBuildups.length > 0) {
        props.filteredBuildups.forEach(index => {
          if (props.buildups[index]) {
            displaySet.add(props.buildups[index]);
          }
        });
      } else {
        // If no filter is applied, display all buildups
        props.buildups.forEach(buildup => displaySet.add(buildup));
      }
      
      // Then add any selected buildups that aren't already included
      props.buildups.forEach(buildup => {
        if (selectedBuildupIds.value.has(buildup.id) && !displaySet.has(buildup)) {
          displaySet.add(buildup);
        }
      });
      
      return Array.from(displaySet);
    });

    // Check if a buildup is in the current filter
    const isInCurrentFilter = (buildup: IBuildup): boolean => {
      if (props.filteredBuildups.length === 0) {
        return true; // No filter applied
      }
      
      return props.filteredBuildups.some(index => props.buildups[index]?.id === buildup.id);
    };

    // Check if a buildup is selected but not in current filter
    const isBuildupSelectedButNotInFilter = (buildup: IBuildup): boolean => {
      return isBuildupSelected(buildup) && !isInCurrentFilter(buildup);
    };

    // Group buildups for display, following the same logic as before
    const groupedDisplayBuildups = computed(() => {
      const grouped: Record<string, Record<string, IBuildup[]>> = {};
      
      displayBuildups.value.forEach(buildup => {
        // Handle each classification entry
        buildup.classification?.forEach(cls => {
          const system = cls.system;
          const codeKey = `${cls.code}|${cls.name}`;
          
          // Initialize system group if it doesn't exist
          if (!grouped[system]) {
            grouped[system] = {};
          }
          
          // Initialize code group if it doesn't exist
          if (!grouped[system][codeKey]) {
            grouped[system][codeKey] = [];
          }
          
          // Add the buildup to the appropriate group
          grouped[system][codeKey].push(buildup);
        });
      });
      
      // Sort each system's code groups by code
      const sortedGrouped: Record<string, Record<string, IBuildup[]>> = {};
      
      Object.keys(grouped).sort().forEach(system => {
        sortedGrouped[system] = {};
        
        // Sort code keys by their numeric code part
        const sortedCodeKeys = Object.keys(grouped[system]).sort((a, b) => {
          const codeA = Number(a.split('|')[0]);
          const codeB = Number(b.split('|')[0]);
          return codeA - codeB;
        });
        
        sortedCodeKeys.forEach(codeKey => {
          sortedGrouped[system][codeKey] = grouped[system][codeKey];
        });
      });
      
      return sortedGrouped;
    });

    

    watch(() => props.buildups, () => {
      // Clear selections when buildups change fundamentally
      if (props.selectedBuildups.length === 0 ) {
        selectedBuildupIds.value.clear();
        selectedCodeGroups.value.clear();
      }

      // Re-check code group selections
      updateCodeGroupSelections();
    }, { deep: true });

    watch(() => props.selectedBuildups, (newSelectedBuildups) => {
        // Only process if we actually have explicit selected buildups
      if (newSelectedBuildups && newSelectedBuildups.length > 0 ) {
      // Convert the indices to IDs for proper comparison
      const newSelectedIds = newSelectedBuildups.map(index => {
        return props.buildups[index]?.id;
      }).filter(id => id !== undefined);

      // Get current selection as an array
      const currentSelectedIds = Array.from(selectedBuildupIds.value);

      // Only update if there's a difference
      if (newSelectedIds.length !== currentSelectedIds.length || 
          !newSelectedIds.every(id => selectedBuildupIds.value.has(id))) {
          
        // Reset and update from parent
        selectedBuildupIds.value.clear();
        newSelectedIds.forEach(id => {
          if (id) selectedBuildupIds.value.add(id);
        });

        // Update code group selections
        updateCodeGroupSelections();
      }
    }
      // If we have an empty array of filtered buildups, clear all selections
      else if (newSelectedBuildups && newSelectedBuildups.length === 0) {
        selectedBuildupIds.value.clear();
        selectedCodeGroups.value.clear();
    }
  },
    { deep: true });

    // Method to check if a buildup is selected
    const isBuildupSelected = (buildup : IBuildup) => {
      return selectedBuildupIds.value.has(buildup.id);
    };

    // Method to check if an entire code group is selected
    const isCodeGroupSelected = (codeKey : string) => {
      return selectedCodeGroups.value.has(codeKey);
    };

    // Group buildups by classification system, then by code+name
    const groupedBuildups = computed(() => {
      const grouped: Record<string, Record<string, IBuildup[]>> = {};
      
      props.buildups.forEach(buildup => {
        // Handle each classification entry
        buildup.classification?.forEach(cls => {
          const system = cls.system;
          const codeKey = `${cls.code}|${cls.name}`;
          
          // Initialize system group if it doesn't exist
          if (!grouped[system]) {
            grouped[system] = {};
          }
          
          // Initialize code group if it doesn't exist
          if (!grouped[system][codeKey]) {
            grouped[system][codeKey] = [];
          }
          
          // Add the buildup to the appropriate group
          grouped[system][codeKey].push(buildup);
        });
      });
      
      // Sort each system's code groups by code
      const sortedGrouped: Record<string, Record<string, IBuildup[]>> = {};
      
      Object.keys(grouped).sort().forEach(system => {
        sortedGrouped[system] = {};
        
        // Sort code keys by their numeric code part
        const sortedCodeKeys = Object.keys(grouped[system]).sort((a, b) => {
          const codeA = Number(a.split('|')[0]);
          const codeB = Number(b.split('|')[0]);
          return codeA - codeB;
        });
        
        sortedCodeKeys.forEach(codeKey => {
          sortedGrouped[system][codeKey] = grouped[system][codeKey];
        });
      });
      
      return sortedGrouped;
    });

      const isCodeGroupPartiallySelected = (codeKey : string) => {
    // If the entire code group is selected, it's not partially selected
    if (selectedCodeGroups.value.has(codeKey)) {
      return false;
    }

    // Get all buildups in this code group
    const allBuildups : IBuildup[] = [];
    Object.values(groupedBuildups.value).forEach(system => {
      if (system[codeKey]) {
        allBuildups.push(...system[codeKey]);
      }
    });

    // Check if some (but not all) buildups are selected
    const selectedCount = allBuildups.filter(buildup => isBuildupSelected(buildup)).length;
    return selectedCount > 0 && selectedCount < allBuildups.length;
  };

    // Toggle section visibility
    const toggleSection = (sectionId: string) => {
      const section = document.getElementById(sectionId);
      if (section) {
        const content = section.querySelector('.filter-groups-container') as HTMLElement;
        const chevron = section.querySelector('.chevron') as HTMLElement;
        
        if (content.style.display === 'none') {
          content.style.display = 'block';
          chevron.classList.remove('collapse-up');
          chevron.classList.add('collapse-down')

        } else {
          content.style.display = 'none';
          chevron.classList.remove('collapse-down');
          chevron.classList.add('collapse-up')
        }
      }
    };

    // Toggle buildups visibility
    const toggleBuildups = (sectionId: string, codeKey: string) => {
  if (expandedCodeGroups.value.has(codeKey)) {
    expandedCodeGroups.value.delete(codeKey);
  } else {
    expandedCodeGroups.value.add(codeKey);
  }
};

    // Method to handle buildup selection

    const emitSelectedBuildups = () => {
      // Get all selected buildup IDs
      const selectedIds = Array.from(selectedBuildupIds.value);

      // Find all indices where selected buildups appear in the original array
      const selectedIndices = props.buildups
        .map((buildup, index) => ({ buildup, index }))
        .filter(item => selectedIds.includes(item.buildup.id))
        .map(item => item.index);

      console.log('BuildupList: Emitting selected buildup indices:', selectedIndices);
      emit('update:selectedBuildups', selectedIndices);
    };

    const selectBuildup = (buildup : IBuildup) => {
      if (selectedBuildupIds.value.has(buildup.id)) {
        selectedBuildupIds.value.delete(buildup.id);
      } else {
        selectedBuildupIds.value.add(buildup.id);
      }

      // Update code group selections
      updateCodeGroupSelections();

      // Emit updated selection to parent
      emitSelectedBuildups();
    };



    // Method to select all buildups in a code group
    const toggleCodeGroup = (codeKey : string, codeGroup : IBuildup[] ) => {
      if (selectedCodeGroups.value.has(codeKey)) {
        // Deselect the code group
        selectedCodeGroups.value.delete(codeKey);

        // Deselect all buildups in this group
        codeGroup.forEach((buildup : IBuildup)  => {
          selectedBuildupIds.value.delete(buildup.id);
        });
      } else {
        // Select the code group
        selectedCodeGroups.value.add(codeKey);

        // Select all buildups in this group
        codeGroup.forEach((buildup: IBuildup) => {
          selectedBuildupIds.value.add(buildup.id);
        });
      }

      // Emit updated selection to parent
      emitSelectedBuildups();
      updateCodeGroupSelections();
    };


    // Helper to update code group selection state
    const updateCodeGroupSelections = () => {
      selectedCodeGroups.value.clear();
      
      // For each code group in each system
      Object.values(groupedBuildups.value).forEach(systemGroup => {
        Object.entries(systemGroup).forEach(([codeKey, buildups]) => {
          // Check if all buildups in this group are selected
          const allSelected = buildups.every(buildup => 
            selectedBuildupIds.value.has(buildup.id)
          );
          
          if (allSelected && buildups.length > 0) {
            selectedCodeGroups.value.add(codeKey);
          }
        });
      });
    };
    
    return {
      groupedDisplayBuildups,
      expandedCodeGroups,
      toggleSection,
      toggleBuildups,
      selectBuildup,
      isBuildupSelected,
      isCodeGroupSelected,
      toggleCodeGroup,
      emitSelectedBuildups,
      isInCurrentFilter,
      isBuildupSelectedButNotInFilter,
      isCodeGroupPartiallySelected
    };
  }
});
</script>

<style scoped>
  .code-group {
    margin-top: var(--spacing-tiny);
    margin-bottom: var(--spacing-sm)
  }

  .not-in-filter {
  font-style: italic; /* Make text italic */
  color: var(--color-text-grey)
}
</style>