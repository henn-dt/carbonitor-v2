import { ref, type Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import { useBarChartGenerator } from '@/views/shared/Graph/useBarChartGenerator';
import { useScatterPlotGenerator } from '@/views/shared/Graph/useScatterPlotGenerator';
import { usePieChartGenerator } from '@/views/shared/Graph/usePieChartGenerator';
import { useLifeCycleComparisonChart } from '@/views/shared/Graph/useLifeCycleComparisonChart';

export function useGraphGenerator(
  props: {
    precalculatedTable: ColumnDefinition[],
    filteredIndices: number[],
    selectedIndices: number[]
  }, 
  graphContainer: Ref<HTMLElement | null>,
  graphType: Ref<string>,
  config: {
    displayMode: Ref<string>,
    xAxisColumn: Ref<string>,
    yAxisColumn: Ref<string>,
    zAxisColumn: Ref<string>,
    colorBy: Ref<string>,
    sliceBy: Ref<string>,
    valueColumn: Ref<string>,
    selectedUnit: Ref<string>,
    includeEndOfLife?: Ref<boolean> // New config for lifecycle comparison
  }
) {
  // Import sub-generators
  const { generateBarChart, generateLifecycleBarChart } = useBarChartGenerator(props, graphContainer, config);
  const { generateScatterPlot } = useScatterPlotGenerator(props, graphContainer, config);
  const { generatePieChart } = usePieChartGenerator(props, graphContainer, config);
  
  // Import the new lifecycle comparison chart generator
  const { generateLifeCycleComparisonChart } = useLifeCycleComparisonChart(
    props, 
    graphContainer, 
    {
      xAxisColumn: config.xAxisColumn,
      indicatorColumn: config.yAxisColumn,
      includeEndOfLife: config.includeEndOfLife || ref(true)
    }
  );
  
  // Load Plotly.js from CDN
  const loadPlotlyCDN = () => {
    return new Promise<void>((resolve, reject) => {
      if ((window as any).Plotly) {
        resolve();
        return;
      }
      const script = document.createElement('script');
      script.src = 'https://cdn.plot.ly/plotly-2.20.0.min.js';
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load Plotly from CDN'));
      document.head.appendChild(script);
    });
  };
  
  // Generate the appropriate plot based on configuration
  const generatePlot = () => {
    if (!graphContainer.value || !(window as any).Plotly) return;
    
    // Clear existing plot
    (window as any).Plotly.purge(graphContainer.value);
    
    // Determine which indices to use based on display mode and graph type
    let rowIndices: number[] = [];
    
    if (graphType.value === 'pie' || graphType.value === 'lifeCycleComparison') {
      // Pie charts and lifecycle comparison always use selected indices
      rowIndices = props.selectedIndices;
    } else {
      // For other graph types, use the display mode
      switch (config.displayMode.value) {
        case 'filtered':
          rowIndices = props.filteredIndices;
          break;
        case 'selected':
          rowIndices = props.selectedIndices;
          break;
        case 'both':
          // Use filtered indices but mark selected items differently in implementation
          rowIndices = props.filteredIndices;
          break;
      }
    }
    
    // Apply unit filtering if applicable (except for lifecycle comparison)
    const filteredRows = (graphType.value === 'lifeCycleComparison' || !config.selectedUnit.value) 
      ? rowIndices 
      : filterRowsByUnit(rowIndices, config.selectedUnit.value);
    
    if (filteredRows.length === 0) {
      // Display a message when no data
      if (graphContainer.value) {
        graphContainer.value.innerHTML = '<div class="no-data">No data available for the current selection</div>';
      }
      return;
    }
    
    switch(graphType.value) {
      case 'bar':
        if (config.colorBy.value === "lifecycles" && config.yAxisColumn.value.includes('-Total')) {
          generateLifecycleBarChart(filteredRows);
        } else {
          generateBarChart(filteredRows);
        }
        break;
      case 'scatter':
        generateScatterPlot(filteredRows);
        break;
      case 'pie':
        generatePieChart(filteredRows);
        break;
      case 'lifeCycleComparison':
        generateLifeCycleComparisonChart();
        break;
    }
  };

  // Filter rows by unit
  const filterRowsByUnit = (indices: number[], unit: string): number[] => {
    if (!unit) return indices;
    
    const unitColumn = props.precalculatedTable.find(col => col.key === 'epd_declaredUnit');
    if (!unitColumn || !unitColumn.columnValues) return indices;
    
    return indices.filter(index => {
      const unitValue = unitColumn.columnValues?.find(v => v.rowId === index)?.value;
      return unitValue === unit;
    });
  };

  return {
    loadPlotlyCDN,
    generatePlot
  };
}