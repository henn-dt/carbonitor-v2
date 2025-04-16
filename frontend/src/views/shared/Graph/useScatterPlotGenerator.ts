import type { Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';

export function useScatterPlotGenerator(
  props: {
    precalculatedTable: ColumnDefinition[],
    selectedIndices: number[]
  },
  graphContainer: Ref<HTMLElement | null>,
  config: {
    displayMode: Ref<string>,
    xAxisColumn: Ref<string>,
    yAxisColumn: Ref<string>,
    zAxisColumn: Ref<string>,
    colorBy: Ref<string>
  }
) {
  // Generate scatter plot (Ashby-style when 3D is enabled)
  const generateScatterPlot = (rowIndices: number[]) => {
    const xColumn = props.precalculatedTable.find(col => col.key === config.xAxisColumn.value);
    const yColumn = props.precalculatedTable.find(col => col.key === config.yAxisColumn.value);
    const zColumn = config.zAxisColumn.value ? 
      props.precalculatedTable.find(col => col.key === config.zAxisColumn.value) : null;
    const colorColumn = config.colorBy.value !== 'none' ? 
      props.precalculatedTable.find(col => col.key === config.colorBy.value) : null;
    
    if (!xColumn || !yColumn || !xColumn.columnValues || !yColumn.columnValues) return;
    
    // Create the appropriate traces based on config
    const traces: any[] = [];
    
    // Set up for Ashby-style chart if 3D is enabled
    const isAshbyStyle = !!zColumn;
    
    // Handle color groups
    if (colorColumn && colorColumn.columnValues) {
      // Group by color value
      const colorGroups = new Map<string, any[]>();
      
      rowIndices.forEach(rowId => {
        const xValue = xColumn.columnValues?.find(v => v.rowId === rowId)?.value;
        const yValue = yColumn.columnValues?.find(v => v.rowId === rowId)?.value;
        const zValue = zColumn?.columnValues?.find(v => v.rowId === rowId)?.value;
        
        // Skip if any required values are missing
        if (xValue === undefined || yValue === undefined || (isAshbyStyle && zValue === undefined)) {
          return;
        }
        
        const colorValue = colorColumn.columnValues?.find(v => v.rowId === rowId)?.value || 'Unknown';
        
        if (!colorGroups.has(colorValue)) {
          colorGroups.set(colorValue, []);
        }
        
        colorGroups.get(colorValue)!.push({
          x: xValue,
          y: yValue,
          z: zValue,
          rowId: rowId
        });
      });
      
      if (isAshbyStyle) {
        // Create Ashby-style chart with ellipses for each group
        createAshbyStyleTraces(colorGroups, xColumn, yColumn, zColumn!, traces);
      } else {
        // Regular scatter plot with color groups
        createColorGroupTraces(colorGroups, xColumn, yColumn, traces);
      }
    } else {
      // No color grouping - single trace
      createSingleTraces(rowIndices, xColumn, yColumn, zColumn, isAshbyStyle, traces);
    }
    
    // Create layout
    const layout = {
      title: isAshbyStyle ?
        `Ashby Chart: ${xColumn.label} vs ${yColumn.label} (size: ${zColumn!.label})` :
        `Scatter: ${xColumn.label} vs ${yColumn.label}`,
      xaxis: { 
        title: xColumn.label,
        type: xColumn.columnProperties?.type === ColumnType.numeric ? 'log' : 'linear'
      },
      yaxis: { 
        title: yColumn.label,
        type: yColumn.columnProperties?.type === ColumnType.numeric ? 'log' : 'linear'
      },
      hovermode: 'closest',
      legend: { orientation: 'h' }
    };
    
    if (graphContainer.value) {
      (window as any).Plotly.newPlot(graphContainer.value, traces, layout);
    }
  };

  // Create Ashby-style traces with ellipses for each group
  const createAshbyStyleTraces = (
    colorGroups: Map<string, any[]>,
    xColumn: ColumnDefinition,
    yColumn: ColumnDefinition,
    zColumn: ColumnDefinition,
    traces: any[]
  ) => {
    colorGroups.forEach((points, colorValue) => {
      // For Ashby style, we need to create both scatter points and ellipses
      
      // 1. Create the scatter points
      const x = points.map(p => p.x);
      const y = points.map(p => p.y);
      const z = points.map(p => p.z);
      
      const scatterTrace = {
        type: 'scatter',
        mode: 'markers',
        x: x,
        y: y,
        name: colorValue,
        legendgroup: colorValue,
        hoverinfo: 'text',
        text: points.map(p => 
          `${colorValue}<br>${xColumn.label}: ${p.x}<br>${yColumn.label}: ${p.y}<br>${zColumn.label}: ${p.z}`
        ),
        marker: {
          size: z.map(zVal => {
            // Normalize between 5 and 25
            const min = Math.min(...z);
            const max = Math.max(...z);
            const range = max - min;
            return range === 0 ? 10 : 5 + (20 * (zVal - min) / range);
          }),
          opacity: 0.7,
          line: {
            color: 'rgba(0,0,0,0.3)',
            width: 1
          }
        }
      };
      
      traces.push(scatterTrace);
      
      // 2. Create the ellipse - if we have more than 3 points
      if (points.length > 3) {
        try {
          // Calculate the ellipse boundary points - simplified approach
          // using standard deviation as a basis for the ellipse size
          const xMean = x.reduce((sum, val) => sum + val, 0) / x.length;
          const yMean = y.reduce((sum, val) => sum + val, 0) / y.length;
          
          const xStd = Math.sqrt(x.reduce((sum, val) => sum + (val - xMean) ** 2, 0) / x.length) * 1.5;
          const yStd = Math.sqrt(y.reduce((sum, val) => sum + (val - yMean) ** 2, 0) / y.length) * 1.5;
          
          // Generate points for an ellipse
          const ellipsePoints = 50;
          const ellipseX = [];
          const ellipseY = [];
          
          for (let i = 0; i < ellipsePoints; i++) {
            const angle = (i / ellipsePoints) * 2 * Math.PI;
            ellipseX.push(xMean + xStd * Math.cos(angle));
            ellipseY.push(yMean + yStd * Math.sin(angle));
          }
          
          // Close the ellipse
          ellipseX.push(ellipseX[0]);
          ellipseY.push(ellipseY[0]);
          
          const ellipseTrace = {
            type: 'scatter',
            mode: 'lines',
            x: ellipseX,
            y: ellipseY,
            name: colorValue,
            legendgroup: colorValue,
            showlegend: false,
            line: {
              color: scatterTrace.marker.line.color,
              width: 2
            },
            opacity: 0.3,
            fill: 'toself',
            hoverinfo: 'none'
          };
          
          traces.push(ellipseTrace);
        } catch (e) {
          console.error("Error creating ellipse:", e);
        }
      }
    });
  };

  // Create regular scatter traces with color grouping
  const createColorGroupTraces = (
    colorGroups: Map<string, any[]>,
    xColumn: ColumnDefinition,
    yColumn: ColumnDefinition,
    traces: any[]
  ) => {
    // Check if we should highlight selected points
    const isHighlightingSelected = config.displayMode.value === 'both';
    const selectedSet = new Set(props.selectedIndices);
    
    colorGroups.forEach((points, colorValue) => {
      // Check if any points in this group are selected
      const hasSelectedPoints = points.some(p => selectedSet.has(p.rowId));
      const isSelectedGroup = isHighlightingSelected && hasSelectedPoints;
      
      traces.push({
        type: 'scatter',
        mode: 'markers',
        x: points.map(p => p.x),
        y: points.map(p => p.y),
        name: isSelectedGroup ? `${colorValue} (Selected)` : colorValue,
        hoverinfo: 'text',
        text: points.map(p => 
          `${colorValue}<br>${xColumn.label}: ${p.x}<br>${yColumn.label}: ${p.y}`
        ),
        marker: {
          size: 10,
          color: isSelectedGroup ? '#ff7f0e' : undefined,
          line: {
            width: isSelectedGroup ? 2 : 1,
            color: isSelectedGroup ? 'black' : 'rgba(0,0,0,0.3)'
          }
        },
        opacity: isSelectedGroup ? 1 : 0.7
      });
    });
  };

  // Create single trace (no color grouping)
  const createSingleTraces = (
    rowIndices: number[],
    xColumn: ColumnDefinition,
    yColumn: ColumnDefinition,
    zColumn: ColumnDefinition | null | undefined,
    isAshbyStyle: boolean,
    traces: any[]
  ) => {
    const points: any[] = [];
    
    rowIndices.forEach(rowId => {
      const xValue = xColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      const yValue = yColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      const zValue = zColumn?.columnValues?.find(v => v.rowId === rowId)?.value;
      
      // Skip if any required values are missing
      if (xValue === undefined || yValue === undefined || (isAshbyStyle && zValue === undefined)) {
        return;
      }
      
      points.push({
        x: xValue,
        y: yValue,
        z: zValue,
        rowId: rowId
      });
    });
    
    if (isAshbyStyle) {
      // Create Ashby-style chart
      const x = points.map(p => p.x);
      const y = points.map(p => p.y);
      const z = points.map(p => p.z);
      
      const scatterTrace = {
        type: 'scatter',
        mode: 'markers',
        x: x,
        y: y,
        hoverinfo: 'text',
        text: points.map(p => 
          `${xColumn.label}: ${p.x}<br>${yColumn.label}: ${p.y}<br>${zColumn!.label}: ${p.z}`
        ),
        marker: {
          size: z.map(zVal => {
            // Normalize between 5 and 25
            const min = Math.min(...z);
            const max = Math.max(...z);
            const range = max - min;
            return range === 0 ? 10 : 5 + (20 * (zVal - min) / range);
          }),
          opacity: 0.7,
          color: z,
          colorscale: 'Viridis',
          showscale: true,
          colorbar: {
            title: zColumn!.label
          },
          line: {
            color: 'rgba(0,0,0,0.3)',
            width: 1
          }
        }
      };
      
      traces.push(scatterTrace);
      
      // Only create ellipse if we have many points
      if (points.length > 5) {
        createEllipseTrace(x, y, traces);
      }
    } else {
      // Regular scatter plot
      traces.push({
        type: 'scatter',
        mode: 'markers',
        x: points.map(p => p.x),
        y: points.map(p => p.y),
        hoverinfo: 'text',
        text: points.map(p => 
          `${xColumn.label}: ${p.x}<br>${yColumn.label}: ${p.y}`
        )
      });
    }
  };

  // Helper function to create ellipse trace
  const createEllipseTrace = (x: any[], y: any[], traces: any[]) => {
    try {
      // Calculate the ellipse boundary
      const xMean = x.reduce((sum, val) => sum + val, 0) / x.length;
      const yMean = y.reduce((sum, val) => sum + val, 0) / y.length;
      
      const xStd = Math.sqrt(x.reduce((sum, val) => sum + (val - xMean) ** 2, 0) / x.length) * 1.5;
      const yStd = Math.sqrt(y.reduce((sum, val) => sum + (val - yMean) ** 2, 0) / y.length) * 1.5;
      
      // Generate points for an ellipse
      const ellipsePoints = 50;
      const ellipseX = [];
      const ellipseY = [];
      
      for (let i = 0; i < ellipsePoints; i++) {
        const angle = (i / ellipsePoints) * 2 * Math.PI;
        ellipseX.push(xMean + xStd * Math.cos(angle));
        ellipseY.push(yMean + yStd * Math.sin(angle));
      }
      
      // Close the ellipse
      ellipseX.push(ellipseX[0]);
      ellipseY.push(ellipseY[0]);
      
      const ellipseTrace = {
        type: 'scatter',
        mode: 'lines',
        x: ellipseX,
        y: ellipseY,
        showlegend: false,
        line: {
          color: 'rgba(100,100,100,0.5)',
          width: 2
        },
        opacity: 0.3,
        fill: 'toself',
        hoverinfo: 'none'
      };
      
      traces.push(ellipseTrace);
    } catch (e) {
      console.error("Error creating ellipse:", e);
    }
  };

  return {
    generateScatterPlot
  };
}