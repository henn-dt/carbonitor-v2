import type { Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export function usePieChartGenerator(
  props: {
    precalculatedTable: ColumnDefinition[],
    selectedIndices: number[]
  },
  graphContainer: Ref<HTMLElement | null>,
  config: {
    sliceBy: Ref<string>,
    valueColumn: Ref<string>
  }
) {
  // Generate pie chart
  const generatePieChart = (rowIndices: number[]) => {
    // For pie charts, we only use selected items
    const selectedRowIndices = props.selectedIndices;
    
    if (selectedRowIndices.length === 0) {
      if (graphContainer.value) {
        graphContainer.value.innerHTML = '<div class="no-data">Please select products to display in the pie chart</div>';
      }
      return;
    }
    
    const sliceColumn = props.precalculatedTable.find(col => col.key === config.sliceBy.value);
    const valueColumn = props.precalculatedTable.find(col => col.key === config.valueColumn.value);
    
    if (!sliceColumn || !valueColumn || !sliceColumn.columnValues || !valueColumn.columnValues) return;
    
    // Group by slice category
    const sliceGroups = new Map<string, number>();
    
    selectedRowIndices.forEach(rowId => {
      const sliceValue = sliceColumn.columnValues?.find(v => v.rowId === rowId)?.value || 'Unknown';
      const numValue = valueColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      
      if (numValue !== undefined && numValue !== null) {
        const currentValue = sliceGroups.get(sliceValue) || 0;
        sliceGroups.set(sliceValue, currentValue + Number(numValue));
      }
    });
    
    if (sliceGroups.size === 0) {
      if (graphContainer.value) {
        graphContainer.value.innerHTML = '<div class="no-data">No valid data available for the selected products</div>';
      }
      return;
    }
    
    // Convert map to arrays for Plotly
    const labels = Array.from(sliceGroups.keys());
    const values = Array.from(sliceGroups.values());
    
    // Create a more vibrant color scale for the pie
    const colors = [
      '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
      '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5'
    ];
    
    const trace = {
      type: 'pie',
      labels,
      values,
      hole: 0.4, // Create a donut chart for better visibility
      hoverinfo: 'label+percent+value',
      textinfo: 'label+percent',
      textposition: 'inside',
      insidetextorientation: 'radial',
      marker: {
        colors: colors.slice(0, labels.length)
      },
      pull: 0.03, // Slightly pull slices apart
    };
    
    const layout = {
      title: `${valueColumn.label} by ${sliceColumn.label}`,
      height: 500,
      margin: { l: 50, r: 50, t: 50, b: 50 }
    };
    
    if (graphContainer.value) {
      (window as any).Plotly.newPlot(graphContainer.value, [trace], layout);
    }
  };

  return {
    generatePieChart
  };
}