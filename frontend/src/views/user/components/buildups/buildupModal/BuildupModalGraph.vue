<template>
    <div class="buildup-modal-graph">
  
      <div class="graph-row" :class="{ 'column': isTall }" ref="graphRow">
        <div class="graph-item treemap">
            <ControlBarContainer>
          <ControlGroup>
            <GraphGroupByDropdown
              :sliceBy="sliceBy"
              @update:sliceBy="setSliceBy"
            />
            <ControlButton
              :title="colorByTitle"
              :class="colorBy === 'lifecycles' ? 'icon lifecycle_color' : 'icon material_color'"
              @click="toggleColorByPhase"
              >
              <span :class="colorBy === 'lifecycles' ? 'icon lifecycle_color' : 'icon material_color'">
              </span>
            </ControlButton>
          </ControlGroup>
        </ControlBarContainer>
          <div ref="treemapContainer" class="graph-plot-container"></div>
        </div>
<!--         <div class="graph-item bar">
          <div ref="barContainer" class="graph-plot-container"></div>
        </div> -->
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, computed, onMounted, onBeforeUnmount, nextTick } from 'vue';
  import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
  import ControlBarContainer from '@/views/shared/ControlButtons/ControlBarContainer.vue';
  import ControlGroup from '@/views/shared/ControlButtons/ControlGroup.vue';
  import ControlButton from '@/views/shared/ControlButtons/ControlButton.vue'

  import GraphGroupByDropdown from '@/views/shared/Graph/GraphGroupByDropdown.vue'

  import { loadPlotlyCDN } from '@/views/shared/Graph/useGraphGenerator';
  
  import { useTreemapGraphGenerator } from '@/views/shared/Graph/useTreemapGraph';
  import { useBarChartGenerator } from '@/views/shared/Graph/useBarChartGenerator';

  const emit = defineEmits(['update:sliceBy', 'update:colorBy', 'selectMappingElement']);
  const props = defineProps<{
    precalculatedTable: ColumnDefinition[],
    filteredIndices: number[],
    selectedIndices: number[],
    selectedIndicator: string,
  }>();

  // Generator




  // State for controls
  const sliceBy = ref<'mappingElement'|'productName'>('mappingElement'); // default to mapping
  const colorBy = ref<string>('mappingElement'); // or "lifeCycle"

  const groupByLabel = computed(() => {
    if (sliceBy.value === 'productName') return 'product'
    return 'group'
    
  })

  const colorByTitle = computed(() =>
    colorBy.value === 'lifecycles'
    ? `Colored by life cycle phase. Click to color by ${groupByLabel.value} instead.`
    : `Colored by ${groupByLabel.value}. Click to color by phase.`
    )

function toggleColorByPhase() {
        
    if (colorBy.value === 'lifecycles') {
        console.log('switch off lifecycles colors')
        colorBy.value = sliceBy.value
        emit('update:colorBy', 'lifecycles')
    } else {
        console.log('switch on lifecycles colors')
        colorBy.value = 'lifecycles'
        emit('update:colorBy', sliceBy)
    }
    
    }

  
  // For demo: valueColumn should be set by context (could be a prop or another control)
  // This is your Impact Indicator key, e.g. "gwp"
  const valueColumn = computed(() => props.selectedIndicator || 'gwp');

  
  // Graph containers
  const treemapContainer = ref<HTMLElement | null>(null);
  const barContainer = ref<HTMLElement | null>(null);
  
  // Flex direction switching logic
  const graphRow = ref<HTMLElement | null>(null);
  const isTall = ref(false);
  
  function updateFlexDirection() {
  // Use the bounding box of the outer container
  const parent = graphRow.value?.parentElement;
  const rect = parent ? parent.getBoundingClientRect() : (graphRow.value ? graphRow.value.getBoundingClientRect() : { width:1, height:1 });
  isTall.value = rect.height > 1.5 * rect.width;
}

function resizeTreemap() {
  if (treemapContainer.value && (window as any).Plotly) {
    (window as any).Plotly.Plots.resize(treemapContainer.value);
  }
}

let ro : ResizeObserver | undefined;
  onMounted(async() => {
    await loadPlotlyCDN()

    nextTick(() => {
        generateTreemapGraph(props.selectedIndices);
        });
        ro = new ResizeObserver(() => { resizeTreemap(); updateFlexDirection(); });
        if (treemapContainer.value) ro.observe(treemapContainer.value);


  });

  onBeforeUnmount(() => {
    ro && ro.disconnect();
  });
  
  watch(graphRow, () => { resizeTreemap(); updateFlexDirection(); });
  watch([() => props.selectedIndices, () => props.precalculatedTable], () => { resizeTreemap(); updateFlexDirection(); } );
  
  function setSliceBy(val: string) {
    sliceBy.value = (val === 'productName' ? 'productName' : 'mappingElement');
    if (colorBy.value !== 'lifecycles') colorBy.value = sliceBy.value;
  }
  function setColorBy(val: string) {
    colorBy.value = val;
  }
  
  // --- Generators
  
  const treemapConfig = {
    sliceBy,
    colorBy,
    valueColumn
  };
  const barConfig = {
    displayMode: ref('selected'),
    xAxisColumn: sliceBy, // grouping for X axis (product or mapping)
    yAxisColumn: computed(() =>
      colorBy.value === 'lifecycles'
        ? `${valueColumn.value}-Total` // fallback, adjust as needed for your bar chart
        : `${valueColumn.value}-Total`
    ),
    colorBy
  };

  const { generateTreemapGraph } =

    useTreemapGraphGenerator(props, treemapContainer, treemapConfig, emit);
  
  const { generateBarChart } =
    useBarChartGenerator(props, barContainer, barConfig);
  
  
  // --- Render both graphs on control/data change
  
  function renderBothGraphs() {
    generateTreemapGraph(props.selectedIndices);
    generateBarChart(props.selectedIndices);
  }
  
  watch(
    [sliceBy, colorBy, valueColumn, () => props.precalculatedTable, () => props.selectedIndices],
    () => {
    generateTreemapGraph(props.selectedIndices);;
      nextTick(updateFlexDirection);
    },
    { deep: true }
  );
  
  </script>
  
  <style scoped>
  .buildup-modal-graph {
    position: relative;
    display: block;
    overflow: hidden;
    max-width: 100%;
    max-height: 100%;
    margin-bottom: var(--spacing-sm);
  }
  
  .graph-row {
    position: relative;
    display: flex;
    flex-direction: row;
    height: 380px !important;
    width: 100%;
    max-height: 100%;
    margin-top: 1.2rem;
  }
  
  .graph-row.column {
    flex-direction: column !important;
  }
  
  .graph-item {
    position: relative;
    min-height: 0 !important;
    max-height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .controls {
    margin-bottom: 1.5rem;
  }
  </style>