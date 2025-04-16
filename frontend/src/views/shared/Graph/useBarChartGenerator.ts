import type { Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export function useBarChartGenerator(
  props: {
    precalculatedTable: ColumnDefinition[],
    selectedIndices: number[]
  },
  graphContainer: Ref<HTMLElement | null>,
  config: {
    displayMode: Ref<string>,
    xAxisColumn: Ref<string>,
    yAxisColumn: Ref<string>,
    colorBy: Ref<string>
  }
) {
  // Generate standard bar chart
  const generateBarChart = (rowIndices: number[]) => {
    const xColumn = props.precalculatedTable.find(col => col.key === config.xAxisColumn.value);
    const yColumn = props.precalculatedTable.find(col => col.key === config.yAxisColumn.value);
    const colorColumn = config.colorBy.value !== 'none' ? props.precalculatedTable.find(col => col.key === config.colorBy.value) : null;
    
    // First level of aggregation: group by xValue
    const xGroups = new Map<string, { yValues: number[], rowIds: number[], colorValues: Map<string, number[]> }>();
    
    if (!xColumn || !yColumn || !xColumn.columnValues || !yColumn.columnValues) return;
    
    // Check if we're in 'both' mode to highlight selected items
    const isHighlightingSelected = config.displayMode.value === 'both';
    const selectedSet = new Set(props.selectedIndices);
    
    // First pass: Create the x-based grouping
    rowIndices.forEach(rowId => {
      const xValue = xColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      const yValue = yColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      const colorValue = colorColumn?.columnValues?.find(v => v.rowId === rowId)?.value || 'Default';
      
      if (xValue !== undefined && yValue !== undefined) {
        if (!xGroups.has(xValue)) {
          xGroups.set(xValue, { 
            yValues: [], 
            rowIds: [], 
            colorValues: new Map<string, number[]>() 
          });
        }
        
        const group = xGroups.get(xValue)!;
        group.yValues.push(yValue);
        group.rowIds.push(rowId);
        
        // Also track the y-values by color for this x-value
        if (!group.colorValues.has(colorValue)) {
          group.colorValues.set(colorValue, []);
        }
        group.colorValues.get(colorValue)!.push(yValue);
      }
    });
    
    const traces: any[] = [];
    
    if (colorColumn && colorColumn.columnValues) {
      // Second level of aggregation: organize by color while respecting x-group aggregation
      const colorGroups = new Map<string, { x: string[], y: number[], isSelected: boolean[] }>();
      
      // Process each x-group
      for (const [xValue, xGroup] of xGroups.entries()) {
        // Check if this x-group has any selected items
        const hasSelectedItems = xGroup.rowIds.some(id => selectedSet.has(id));
        
        // Process each color within this x-group
        for (const [colorValue, yValues] of xGroup.colorValues.entries()) {
          // Calculate the mean for this color within this x-group
          const meanValue = yValues.reduce((sum, val) => sum + val, 0) / yValues.length;
          
          // Determine the group key based on selection status
          const groupKey = isHighlightingSelected && hasSelectedItems 
            ? `${colorValue} (Selected)` 
            : colorValue;
          
          if (!colorGroups.has(groupKey)) {
            colorGroups.set(groupKey, { x: [], y: [], isSelected: [] });
          }
          
          const group = colorGroups.get(groupKey)!;
          group.x.push(xValue);
          group.y.push(meanValue);
          group.isSelected.push(hasSelectedItems);
        }
      }
      
      // Create traces from color groups
      colorGroups.forEach((data, colorValue) => {
        const isSelectedGroup = colorValue.includes('(Selected)');
        
        traces.push({
          type: 'bar',
          x: data.x,
          y: data.y,
          name: colorValue,
          marker: {
            color: isSelectedGroup ? '#ff7f0e' : undefined, // Highlight selected
            line: {
              width: isSelectedGroup ? 2 : 0,
              color: isSelectedGroup ? 'black' : undefined
            }
          },
          opacity: isSelectedGroup ? 1 : 0.7
        });
      });
    } else {
      // When not grouping by color - keep this part as is
      if (isHighlightingSelected) {
        // Create separate traces for selected and non-selected items
        const selectedX: any[] = [];
        const selectedY: any[] = [];
        const nonSelectedX: any[] = [];
        const nonSelectedY: any[] = [];
        
        for (const [xValue, xGroup] of xGroups.entries()) {
          // Calculate mean y-value for this x-group
          const meanYValue = xGroup.yValues.reduce((sum, val) => sum + val, 0) / xGroup.yValues.length;
          
          // Check if this x-group has any selected items
          const hasSelectedItems = xGroup.rowIds.some(id => selectedSet.has(id));
          
          if (hasSelectedItems) {
            selectedX.push(xValue);
            selectedY.push(meanYValue);
          } else {
            nonSelectedX.push(xValue);
            nonSelectedY.push(meanYValue);
          }
        }
        
        // Non-selected items trace
        if (nonSelectedX.length > 0) {
          traces.push({
            type: 'bar',
            x: nonSelectedX,
            y: nonSelectedY,
            name: 'Filtered',
            opacity: 0.7
          });
        }
        
        // Selected items trace
        if (selectedX.length > 0) {
          traces.push({
            type: 'bar',
            x: selectedX,
            y: selectedY,
            name: 'Selected',
            marker: {
              color: '#ff7f0e',
              line: {
                width: 2,
                color: 'black'
              }
            }
          });
        }
      } else {
        // Single trace without selection highlighting
        const x: string[] = [];
        const y: number[] = [];
        
        for (const [xValue, xGroup] of xGroups.entries()) {
          const meanYValue = xGroup.yValues.reduce((sum, val) => sum + val, 0) / xGroup.yValues.length;
          x.push(xValue);
          y.push(meanYValue);
        }
        
        traces.push({
          type: 'bar',
          x,
          y
        });
      }
    }
    
    const layout = {
      title: `${yColumn.label} by ${xColumn.label}`,
      xaxis: { title: xColumn.label },
      yaxis: { title: yColumn.label },
      barmode: 'group',
      legend: { orientation: 'h' }
    };
    
    if (graphContainer.value) {
      (window as any).Plotly.newPlot(graphContainer.value, traces, layout);
    }
  };
  
  // Generate lifecycle breakdown bar chart
  const generateLifecycleBarChart = (rowIndices: number[]) => {
    const xColumn = props.precalculatedTable.find(col => col.key === config.xAxisColumn.value);
    const totalColumn = props.precalculatedTable.find(col => col.key === config.yAxisColumn.value);
    
    if (!xColumn || !totalColumn || !xColumn.columnValues || !totalColumn.columnValues) return;
    
    // Extract the indicator key from the Total column
    const indicatorKey = totalColumn.key.split('-')[0];
    
    // Find all lifecycle columns for this indicator
    const lifecycleColumns = props.precalculatedTable.filter(col => 
      col.key.startsWith(indicatorKey + '-') && 
      !col.key.endsWith('-Total') && 
      !col.key.endsWith('-Reuse')
    );
    
    // First level aggregation: group by xValue
    // For each x-value, we'll store the values for each lifecycle stage
    type LifecycleData = {
      [lifecycle: string]: number[];
    };
    
    const xGroups = new Map<string, LifecycleData>();
    
    // First pass: aggregate data by x-value
    rowIndices.forEach(rowId => {
      const xValue = xColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      
      if (xValue !== undefined) {
        if (!xGroups.has(xValue)) {
          xGroups.set(xValue, {});
        }
        
        const xGroup = xGroups.get(xValue)!;
        
        // Process each lifecycle column for this row
        lifecycleColumns.forEach(lifecycleCol => {
          const lifecycle = lifecycleCol.key.split('-')[1];
          const yValue = lifecycleCol.columnValues?.find(v => v.rowId === rowId)?.value;
          
          if (yValue !== undefined) {
            if (!xGroup[lifecycle]) {
              xGroup[lifecycle] = [];
            }
            xGroup[lifecycle].push(yValue);
          }
        });
      }
    });
    
    // Now create traces using the aggregated data
    const traces: any[] = [];
    
    // Create a data structure to hold the final aggregated values
    type TraceData = {
      [lifecycle: string]: {
        x: string[];
        y: number[];
      };
    };
    
    const traceData: TraceData = {};
    
    // Initialize trace data for each lifecycle stage
    lifecycleColumns.forEach(lifecycleCol => {
      const lifecycle = lifecycleCol.key.split('-')[1];
      traceData[lifecycle] = {
        x: [],
        y: []
      };
    });
    
    // Calculate means for each lifecycle stage within each x-group
    for (const [xValue, lifecycles] of xGroups.entries()) {
      for (const lifecycle in lifecycles) {
        const values = lifecycles[lifecycle];
        const mean = values.reduce((sum, val) => sum + val, 0) / values.length;
        
        traceData[lifecycle].x.push(xValue);
        traceData[lifecycle].y.push(mean);
      }
    }
    
    // Create a trace for each lifecycle stage
    for (const lifecycle in traceData) {
      const data = traceData[lifecycle];
      traces.push({
        type: 'bar',
        x: data.x,
        y: data.y,
        name: lifecycle
      });
    }
    
    const layout = {
      title: `${totalColumn.label} Breakdown by Lifecycle Stage`,
      xaxis: { title: xColumn.label },
      yaxis: { title: totalColumn.label },
      barmode: 'stack',
      legend: { orientation: 'h' }
    };
    
    if (graphContainer.value) {
      (window as any).Plotly.newPlot(graphContainer.value, traces, layout);
    }
  };

  return {
    generateBarChart,
    generateLifecycleBarChart
  };
}