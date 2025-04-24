import { computed, type Ref , defineEmits} from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

import { useColorStore } from '@/stores/colorStore';

export function useTreemapGraphGenerator(
  props: {
    precalculatedTable: ColumnDefinition[],
    filteredIndices: number[],
    selectedIndices: number[]
  },
  graphContainer: Ref<HTMLElement | null>,
  config: {
    sliceBy: Ref<string>,   // 'mappingElement' | 'productName'
    colorBy: Ref<string>,   // 'lifeCycle' | 'mappingElement' | ...
    valueColumn: Ref<string>
    // ... any other keys as needed
  }, 
  emit: (event: "selectMappingElement", value: string) => void
) {

  const colorStore = useColorStore()

  // Compute grouping and breakdown from sliceBy/colorBy
  const grouping = computed(() => {
    // Accept only these keys; fallback to mappingElement if not
    return config.sliceBy.value === 'productName' ? 'productName' : 'mappingElement';
  }) as Ref<'productName' | 'mappingElement'>;

  const colorByLifeCycle = computed(() => config.colorBy.value === 'lifecycles');

  // Safely get column and value
  function getCol(colKey: string) {
    return props.precalculatedTable.find(col => col.key === colKey);
  }
  function getValue(colKey: string, rowId: number) {
    return getCol(colKey)?.columnValues?.find(r => r.rowId === rowId)?.value;
  }

  // We'll use only the rowIds passed (filtered/selected)
  function generateTreemapGraph(rowIndices: number[]) {
    if (!graphContainer.value || !(window as any).Plotly || !rowIndices.length) return;
  
    const indicatorBase = config.valueColumn.value;    // e.g. "gwp"
    // Find all columns corresponding to phases of the current indicator
    const phaseCols = props.precalculatedTable.filter(col => 
      col.key.startsWith(indicatorBase + '-') && !col.key.endsWith('-Total')
    );
    const phaseNames = phaseCols.map(col => col.key.replace(`${indicatorBase}-`, ''));
  
    // Grouping key: mapping or product
    const groupingKey = grouping.value;  // 'mappingElement' or 'productName'
  
    // First, create a lookup: for each phase, array of grouping keys+totals
    let allNodes = [];
    let ids : string[] = [];
    let labels : string[] = [];
    let parents : string[] = [];
    let values : number[] = [];
    let colors = [];
    let customdata: (string | number | null)[] = [];
  
    // 1. Without breakdown: Just show each group with sum of all phases
    if (!colorByLifeCycle.value) {
      // Root node for the treemap
      ids.push('root');
      labels.push('Total');
      parents.push('');
      values.push(0); // We'll sum this up after adding all children

      let totalSum = 0;
    
        // If grouping by mapping element, show products within each element
  if (grouping.value === 'mappingElement') {
    // Get all unique mapping elements
    const mappingElements = [...new Set(
      rowIndices.map(rowId => getValue('mappingElement', rowId))
    )].filter(name => name !== undefined && name !== null);
    
    // For each mapping element
    mappingElements.forEach((mapping, mapIdx) => {
      // Get all rows for this mapping element
      const rowsForMapping = rowIndices.filter(rid => 
        getValue('mappingElement', rid) === mapping
      );
      
      let mappingTotal = 0;
      
      // Add mapping element node
      ids.push(`mapping-${mapIdx}`);
      labels.push(String(mapping));
      parents.push('root');
      values.push(0); // Placeholder, will update after adding children
      
      
      // Get unique products within this mapping element
      const productsInMapping = [...new Set(
        rowsForMapping.map(rid => getValue('productName', rid))
      )].filter(name => name !== undefined && name !== null);
      
      // For each product in this mapping
      productsInMapping.forEach((product, prodIdx) => {
        // Get rows for this product
        const rowsForProduct = rowsForMapping.filter(rid => 
          getValue('productName', rid) === product
        );
        
        // Calculate product total across all phases
        let productTotal = 0;
        rowsForProduct.forEach(rid => {
          phaseCols.forEach(col => {
            const val = getValue(col.key, rid);
            productTotal += typeof val === "number" ? val : 0;
          });
        });
        
        if (productTotal > 0) {
          ids.push(`mapping-${mapIdx}-product-${prodIdx}`);
          labels.push(String(product));
          parents.push(`mapping-${mapIdx}`);
          values.push(productTotal);
          customdata.push(mapIdx)
          
          mappingTotal += productTotal;
        }
      });
      
      // Update mapping element total
      values[ids.indexOf(`mapping-${mapIdx}`)] = mappingTotal;
      totalSum += mappingTotal;
    });
  } else {

      // For each unique group
      const groupNames = [...new Set(
          rowIndices.map(rowId => getValue(groupingKey, rowId))
      )].filter(name => name !== undefined && name !== null);
      
      
      
      // Add each group as a child of root
      groupNames.forEach((gname, idx) => {
        const rowsForGroup = rowIndices.filter(rid => getValue(groupingKey, rid) === gname);
        let sum = 0;
        
        rowsForGroup.forEach(rid => {
          phaseCols.forEach(col => {
            const val = getValue(col.key, rid);
            sum += typeof val === "number" ? val : 0;
          });
        });
        
        ids.push(`group-${idx}`);
        labels.push(String(gname)); // Ensure labels are strings
        parents.push('root'); // Connect to root instead of empty string
        values.push(sum);
        totalSum += sum;
      });
    }
      
      // Set the correct total for the root node
      values[0] = totalSum;
    } else {
      // 2. With breakdown: root -> phases, each phase -> groups
// First, get all unique group names and phases
const groupNames = [...new Set(
  rowIndices.map(rowId => getValue(groupingKey, rowId))
)].filter(name => name !== undefined && name !== null);

// First add phase nodes as children of root
ids.push('root');
labels.push('Total');
parents.push('');
values.push(0); // Will calculate total later

// Map to store phase totals
let phaseTotals : Record<string , number> = {};
let grandTotal = 0;

// For each phase, add a node
phaseNames.forEach(phase => {
  ids.push(`phase-${phase}`);
  labels.push(phase);
  parents.push('root');
  phaseTotals[phase] = 0; // Initialize phase total
  values.push(0); // Placeholder, will update later
});

// Now, process each group & phase combination
groupNames.forEach((groupName, groupIdx) => {
  // Get all rows for this group
  const rowsForGroup = rowIndices.filter(rid => 
    getValue(groupingKey, rid) === groupName
  );
  
  // For each phase, add a node for this group
  phaseNames.forEach(phase => {
    const phaseColKey = `${indicatorBase}-${phase}`;
    
    // Calculate sum for this group in this phase
    let groupPhaseSum = 0;
    rowsForGroup.forEach(rid => {
      const val = getValue(phaseColKey, rid);
      groupPhaseSum += typeof val === "number" ? val : 0;
    });
    
    // Only add nodes with values
    if (groupPhaseSum > 0) {
      // Use consistent naming that avoids collisions
      const groupId = `group-${groupIdx}-${groupName.replace(/\s+/g, '_')}`;
      const nodeId = `phase-${phase}-${groupId}`;
      
      ids.push(nodeId);
      labels.push(String(groupName));
      parents.push(`phase-${phase}`);
      values.push(groupPhaseSum);
      
      // Add to phase total
      phaseTotals[phase] += groupPhaseSum;
    }
  });
});

// Update all phase totals
phaseNames.forEach(phase => {
  const phaseIndex = ids.indexOf(`phase-${phase}`);
  if (phaseIndex !== -1) {
    values[phaseIndex] = phaseTotals[phase];
    grandTotal += phaseTotals[phase];
  }
});

// Update root total
values[0] = grandTotal;

// Log the data structure for debugging

/* console.log({
  ids: ids,
  labels: labels,
  parents: parents,
  values: values
}); */
    }


    // Update the marker colors for better visualization
    const marker = {
      colors: ids.map((id, i) => {
        // For lifecycle coloring
        if (colorByLifeCycle.value) {
          // Get the phase name from the ID
          let phaseId: string | null = null;
          
          if (id.startsWith('phase-')) {
            // Direct phase node: phase-Production
            phaseId = id.split('-')[1];
          } else if (parents[i].startsWith('phase-')) {
            // Child of a phase: get phase from parent
            phaseId = parents[i].split('-')[1];
          }
          
          if (phaseId) {
            const baseColor = colorStore.getLifecycleColor(phaseId);
            
            // Phase nodes get their base color
            if (id === `phase-${phaseId}`) {
              return baseColor;
            }
            
            // Products under mapping elements get slightly lighter color
            if (parents[i].includes('mapping-') || (parents[i] === `phase-${phaseId}` && !id.includes('mapping-'))) {
              const childColor = colorStore.getLighterLifecycleColor(phaseId, 0.6);
              console.log(childColor)
              return childColor
            }
          }
          
          return null; // Root or other nodes
        } 
        // For non-lifecycle coloring
        else {
          if (id === 'root') return null;
          const label = labels[i];
          
          // When grouping by mapping element
          if (grouping.value === 'mappingElement') {
            // Each mapping element gets a unique color
            if (id.startsWith('mapping-') && id.split('-').length === 2) {
              // Use colorStore if provided & defined
              if (colorStore && colorStore.productMappingColor[label]) return colorStore.productMappingColor[label];
              // Fallback to HSL color otherwise
              const mappingIndex = parseInt(id.split('-')[1]);
              return `hsl(${mappingIndex * 40 % 360}, 70%, 50%)`;
            }
            
            // Products inherit their parent mapping element's color
            if (parents[i].startsWith('mapping-')) {
              const parentLabel = labels[ids.indexOf(parents[i])];
              // Use colorMap for parent mapping element if present, else fallback
              if (colorStore && colorStore.productMappingColor[parentLabel]) return colorStore.productMappingColor[parentLabel];
              // Else fallback to HSL color as parent
              const mappingIndex = parseInt(parents[i].split('-')[1]);
              return `hsl(${mappingIndex * 40 % 360}, 65%, 55%)`;
            }
          } 
          // When grouping by product
          else {
            // Simple color gradient for products
            const maxVal = Math.max(...values.filter((_, idx) => parents[idx] === 'root'));
            const ratio = values[i] / maxVal;
            return `hsl(220, ${Math.round(ratio * 100)}%, ${50 + Math.round((1-ratio) * 30)}%)`;
          }
          
          return null;
        }
      })
    };

    const title = {
      text: `Treemap (${indicatorBase}${colorByLifeCycle.value ? ' by life cycle' : ''})`,
      font: { size: 16 }, // or whatever small size you want
      x: 0.00, // (0.0 is left, 0.5 is center, 1.0 is right)
      xanchor: 'left',
      pad: { t: 8, b: 8, l:44 }, // title padding (top, bottom)
    }

    // --- Plotly trace
    const trace = {
      type: "treemap",
      ids,
      labels,
      parents,
      values,
      customdata,
      branchvalues: "total",
      hoverinfo: "label+value+percent parent+percent entry",
      // If you want each phase a different color:
      marker
    };
    const layout = {
      autosize: true,
      width: null,
      height: null,
      title: title,
      margin: { t: 40, l: 40, b: 20, r: 20 },
    };

    interface PlotlyHTMLElement extends HTMLElement {
      on: (event: string, handler: (e: any) => void) => void;
    }
    (window as any).Plotly.newPlot(graphContainer.value, [trace], layout, { responsive: true }).then(() => {
      const plotlyEl = graphContainer.value as unknown as PlotlyHTMLElement
      if (plotlyEl.on) plotlyEl.on('plotly_click', onTreemapClick)
    });


    function onTreemapClick(e: any) {
      console.log(`clicked on treemap node ${e.points[0].labels}`)
      const point = e.points[0];
      if (grouping.value === 'mappingElement') {
        emit("selectMappingElement", point.label);
      } else if (grouping.value === 'productName') {
        // Get the rowId from customdata
        const rowId = point.customdata;
        // Now look up the mapping element from precalculatedTable
        // (assume you've made this available in your setup)
        const mappingCol = props.precalculatedTable.find(col => col.key === "mappingElement");
        const mappingEntry = mappingCol?.columnValues?.find(row => row.rowId === rowId);
        if (mappingEntry) {
          emit("selectMappingElement", mappingEntry.value);
        }
      }
    }

    
  }



  return {
    generateTreemapGraph

  };
}
