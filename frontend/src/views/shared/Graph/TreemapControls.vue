<template>
    <div class="treemap-bar-controls">
      <!-- Grouping Dropdown -->
      <div class="form-group right custom-dropdown-group">
        <label for="groupByDropdown" class="dropdown-label">Group by</label>
        <div class="dropdown">
          <button class="dropdown-btn" id="groupByDropdown" @click="toggleDropdown" :aria-expanded="dropdownOpen">
            <span class="form-label">{{ currentGroupByLabel }}</span>
            <span class="icon form dropdown"></span>
          </button>
          <div :class="['dropdown', 'popup', dropdownOpen && 'dropdown--visible']" id="dropdownCard">
            <ul class="list">
              <li class="element" @click="selectGroupBy('productName')">
                <span class="icon product"></span>
                <p class="label">Product</p>
              </li>
              <li class="element" @click="selectGroupBy('mappingElement')">
                <span class="icon group"></span>
                <p class="label">Groups</p>
              </li>
            </ul>
          </div>
        </div>
      </div>
  
      <!-- Color By Phase Toggle -->
       <div>
        <label for="lifeCycleCheckbox" class="dropdown-label">color by Phase</label>
        <div class="toggle-group">        
          <label class="switch">
          <!-- Note: use v-model for two-way binding if you want, here only manual handler for demo -->
            <input type="checkbox"
                 class="checkbox"
                 :checked="colorBy === 'lifecycles'"
                 @change="toggleColorByPhase">
            <div class="slider"></div>
          </label>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, watch, computed, onMounted, onBeforeUnmount } from 'vue';


  const props = defineProps<{
    sliceBy: string,
    colorBy: string
  }>();
  const emit = defineEmits(['update:sliceBy', 'update:colorBy']);
  
  // Dropdown menu logic
  const dropdownOpen = ref(false);
  
  const groupOptions = [
    { key: 'productName', label: 'Product' },
    { key: 'mappingElement', label: 'Group' }
  ];
  
  const currentGroupByLabel = computed(() => {
    const found = groupOptions.find(opt => opt.key === props.sliceBy);
    return found ? found.label : props.sliceBy;
  });
  
  function toggleDropdown(event: Event) {
    dropdownOpen.value = !dropdownOpen.value;
    event.stopPropagation();
  }
  function closeDropdown() {
    dropdownOpen.value = false;
  }
  function selectGroupBy(key: string) {
    emit('update:sliceBy', key);
    closeDropdown();
  }
  
  function handleClickOutside(event: MouseEvent) {
    const dropdown = document.getElementById('groupByDropdown');
    const dropdownCard = document.getElementById('dropdownCard');
    if (dropdown && dropdownCard && !dropdown.contains(event.target as Node) && !dropdownCard.contains(event.target as Node)) {
      closeDropdown();
    }
  }
  onMounted(() => {
    window.addEventListener('click', handleClickOutside);
  });
  onBeforeUnmount(() => {
    window.removeEventListener('click', handleClickOutside);
  });
  
  // Toggle logic
  function toggleColorByPhase(event: Event) {
  const checked = (event.target as HTMLInputElement).checked;
  if (checked) {
    emit('update:colorBy', 'lifecycles');
  } else {
    emit('update:colorBy', props.sliceBy);
  }
}
  </script>

<style scoped>
.treemap-bar-controls {
  display: flex;
  align-items: center;
  gap: 2rem;
}
.custom-dropdown-group {
  min-width: 220px;
}

.toggle-group {
  display: flex;
  align-items: center;
  gap: 1em;
}

.toggle-label {
  margin-left: 6px;
  font-size: 1em;
  color: #444;
}

</style>