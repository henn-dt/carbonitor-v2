
import type { Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';

export function useLifeCycleComparisonChart(
  props: {
    precalculatedTable: ColumnDefinition[],
    selectedIndices: number[]
  },
  graphContainer: Ref<HTMLElement | null>,
  config: {
    xAxisColumn: Ref<string>,  // String column for product names
    indicatorColumn: Ref<string>,  // The -Total indicator column
    includeEndOfLife: Ref<boolean> // Whether to include EndOfLife in comparison
  }
) {
  const generateLifeCycleComparisonChart = () => {
    const xColumn = props.precalculatedTable.find(col => col.key === config.xAxisColumn.value);
    const totalColumn = props.precalculatedTable.find(col => col.key === config.indicatorColumn.value);
    
    if (!xColumn || !totalColumn || !xColumn.columnValues || !totalColumn.columnValues) {
      console.error("Required columns not found or missing values");
      return;
    }
    
    // Extract the indicator key from the Total column
    const indicatorKey = totalColumn.key.split('-')[0];
    
    // Determine if we have EndOfLife data
    const endOfLifeKey = `${indicatorKey}-Disposal`;
    const endOfLifeColumn = props.precalculatedTable.find(col => col.key === endOfLifeKey);
    
    // Prepare the chart
    const chartData: {
      product: string;
      fullProductName: string;
      totalValue: number;
      withoutEolValue?: number;
      rowId: number;
    }[] = [];
    
          // Process data for selected products
    props.selectedIndices.forEach(rowId => {
      const xValue = xColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      const totalValue = totalColumn.columnValues?.find(v => v.rowId === rowId)?.value;
      
      if (xValue !== undefined && totalValue !== undefined && typeof totalValue === 'number') {
        const fullProductName = String(xValue);
        // Truncate product name to 10 characters with ellipsis if needed
        const truncatedName = fullProductName.length > 10 
          ? fullProductName.substring(0, 10) + '...' 
          : fullProductName;
          
        const chartItem: {
          product: string;
          fullProductName: string;
          totalValue: number;
          withoutEolValue?: number;
          rowId: number;
        } = {
          product: truncatedName,
          fullProductName: fullProductName,
          totalValue: totalValue,
          rowId: rowId
        };
        
        // If EndOfLife is included, calculate the value without it
        if (config.includeEndOfLife.value && endOfLifeColumn && endOfLifeColumn.columnValues) {
          const eolValue = endOfLifeColumn.columnValues.find(v => v.rowId === rowId)?.value;
          if (eolValue !== undefined && typeof eolValue === 'number') {
            chartItem.withoutEolValue = totalValue - eolValue;
          }
        }
        
        chartData.push(chartItem);
      }
    });
    
    // Sort data by value without disposal (highest first)
    // If withoutEolValue is not available, fall back to totalValue
    chartData.sort((a, b) => {
      const aValue = a.withoutEolValue !== undefined ? a.withoutEolValue : a.totalValue;
      const bValue = b.withoutEolValue !== undefined ? b.withoutEolValue : b.totalValue;
      return bValue - aValue; // Descending order
    });
    
    // Only take the top 4 items
    const topChartData = chartData.slice(0, 4);
    
    // Create custom x-axis values for better positioning control
    const xBase = 1;
    const xStep = 3;
    const xValues = topChartData.map((_, i) => xBase + i * xStep);
    
    // Prepare the traces for Plotly
    const traces: any[] = [];
    
    if (config.includeEndOfLife.value) {
      // First add the total value as a gray bar (shadow effect)
      // Shift it slightly to the left
      const shadowOffset = 0.08; // Small offset to create shadow effect
      
      traces.push({
        type: 'bar',
        x: xValues.map(x => x - shadowOffset), // Slightly offset to the left
        y: topChartData.map(item => item.totalValue),
        width: 0.5, // Width of bars
        name: 'Total (With EndOfLife)',
        marker: {
          color: 'rgba(113, 121, 126, 0.5)', // Semi-transparent gray
          line: {
            width: 0
          }
        },
        hoverinfo: 'text',
        hovertext: topChartData.map(item => 
          `${item.fullProductName}<br>Total: ${item.totalValue.toFixed(2)}`
        )
      });
      
      // Then add the orange bar on top (withoutEolValue)
      traces.push({
        type: 'bar',
        x: xValues, // No offset for orange bars
        y: topChartData.map(item => item.withoutEolValue || 0),
        width: 0.5, // Width of bars
        name: 'Without EndOfLife (A1-A3)',
        marker: {
          color: '#FF8C00', // Orange
          line: {
            width: 1,
            color: 'black'
          }
        },
        hoverinfo: 'text',
        hovertext: topChartData.map(item => 
          `${item.fullProductName}<br>Without EndOfLife: ${(item.withoutEolValue || 0).toFixed(2)}`
        ),
        text: topChartData.map(item => item.product),
        textposition: 'outside'
      });
      
      // Add arrows and percentage lines between CONSECUTIVE bars
      for (let i = 0; i < topChartData.length - 1; i++) {
        const currentItem = topChartData[i];
        const nextItem = topChartData[i + 1];
        
        if (currentItem.withoutEolValue === undefined || nextItem.withoutEolValue === undefined) continue;
        
        const currentX = xValues[i];
        const nextX = xValues[i + 1];
        
        // Calculate reduction percentages
        const totalReduction = ((currentItem.totalValue - nextItem.totalValue) / currentItem.totalValue * 100).toFixed(1);
        const withoutEolReduction = ((currentItem.withoutEolValue - nextItem.withoutEolValue) / currentItem.withoutEolValue * 100).toFixed(1);
        
        // Add dashed horizontal line from the current total value to next total (with disposal)
        traces.push({
          type: 'scatter',
          mode: 'lines',
          x: [currentX - shadowOffset, nextX - shadowOffset], // From current shadow to next shadow
          y: [currentItem.totalValue, currentItem.totalValue],
          line: {
            width: 1,
            color: 'gray',
            dash: 'dash'  // Make the line dashed
          },
          showlegend: false
        });
        
        // Add solid horizontal line from current withoutEol to next withoutEol
        traces.push({
          type: 'scatter',
          mode: 'lines',
          x: [currentX, nextX], // From current orange to next orange
          y: [currentItem.withoutEolValue, currentItem.withoutEolValue],
          line: {
            width: 1,
            color: 'black'
          },
          showlegend: false
        });
        
        // Add text annotation for total reduction (with disposal)
        traces.push({
          type: 'scatter',
          mode: 'text',
          x: [(currentX - shadowOffset + nextX - shadowOffset) / 2],
          y: [currentItem.totalValue + (currentItem.totalValue * 0.05)], // Slightly above the line
          text: [`${totalReduction}% Total Reduktion`],
          textfont: {
            size: 10,
            color: 'gray'
          },
          showlegend: false
        });
        
        // Add text annotation for reduction without disposal
        traces.push({
          type: 'scatter',
          mode: 'text',
          x: [(currentX + nextX) / 2],
          y: [currentItem.withoutEolValue + (currentItem.withoutEolValue * 0.05)], // Slightly above the line
          text: [`${withoutEolReduction}% ${indicatorKey}-Reduktion`],
          textfont: {
            size: 10,
            color: 'black'
          },
          showlegend: false
        });
      }
      
      // For each bar, add the vertical cutted line with arrow
      topChartData.forEach((item, index) => {
        if (item.withoutEolValue === undefined) return;
        
        const xPos = xValues[index];
        const shadowOffset = 0.08; // Small offset to create shadow effect
        const xPosShadow = xPos - shadowOffset;
        
        // Add vertical dashed line from withoutEol to total
        traces.push({
          type: 'scatter',
          mode: 'lines',
          x: [xPosShadow, xPosShadow], // Vertical line at shadow position
          y: [item.withoutEolValue, item.totalValue],
          line: {
            width: 1,
            color: 'gray',
            dash: 'dash'  // Make the line dashed
          },
          showlegend: false
        });
        
        // Calculate disposal percentage
        const disposalPercentage = ((item.totalValue - item.withoutEolValue) / item.totalValue * 100).toFixed(1);
        
        // Add disposal percentage text
        traces.push({
          type: 'scatter',
          mode: 'text',
          x: [xPosShadow - 0.4], // Slightly to the left of the bar
          y: [(item.withoutEolValue + item.totalValue) / 2],
          text: [`${disposalPercentage}%<br>Disposal`],
          textfont: {
            size: 9,
            color: 'gray'
          },
          showlegend: false
        });
      });
      
      // Add disposal reduction comparisons between consecutive bars
      for (let i = 0; i < topChartData.length - 1; i++) {
        const currentItem = topChartData[i];
        const nextItem = topChartData[i + 1];
        
        if (currentItem.withoutEolValue === undefined || nextItem.withoutEolValue === undefined) continue;
        
        const currentX = xValues[i];
        const nextX = xValues[i + 1];
        const shadowOffset = 0.08;
        
        // Calculate disposal components
        const currentDisposal = currentItem.totalValue - currentItem.withoutEolValue;
        const nextDisposal = nextItem.totalValue - nextItem.withoutEolValue;
        
        // Calculate disposal reduction percentage
        if (currentDisposal > 0) {  // Avoid division by zero
          const disposalReductionPct = ((currentDisposal - nextDisposal) / currentDisposal * 100).toFixed(1);
          
          // Add disposal reduction text
          traces.push({
            type: 'scatter',
            mode: 'text',
            x: [(currentX + nextX) / 2 - shadowOffset],
            y: [(currentItem.totalValue + nextItem.totalValue) / 2],
            text: [`${disposalReductionPct}%<br>Disposal Reduktion`],
            textfont: {
              size: 9,
              color: 'gray'
            },
            showlegend: false
          });
        }
      }
    } else {
      // Just show single bars without EndOfLife comparison
      traces.push({
        type: 'bar',
        x: xValues,
        y: topChartData.map(item => item.totalValue),
        width: 0.5,
        name: totalColumn.label,
        marker: {
          color: '#FF8C00', // Orange
          line: {
            width: 1,
            color: 'black'
          }
        },
        hoverinfo: 'text',
        hovertext: topChartData.map(item => 
          `${item.fullProductName}<br>${totalColumn.label}: ${item.totalValue.toFixed(2)}`
        ),
        text: topChartData.map(item => item.product),
        textposition: 'outside',
      });
      
      // Add reduction arrows between consecutive bars
      for (let i = 0; i < topChartData.length - 1; i++) {
        const currentItem = topChartData[i];
        const nextItem = topChartData[i + 1];
        
        const currentX = xValues[i];
        const nextX = xValues[i + 1];
        
        // Calculate reduction percentage
        const reduction = ((currentItem.totalValue - nextItem.totalValue) / currentItem.totalValue * 100).toFixed(1);
        
        // Add horizontal line
        traces.push({
          type: 'scatter',
          mode: 'lines',
          x: [currentX, nextX],
          y: [currentItem.totalValue, currentItem.totalValue],
          line: {
            width: 1,
            color: 'black'
          },
          showlegend: false
        });
        
        // Add text annotation for reduction
        traces.push({
          type: 'scatter',
          mode: 'text',
          x: [(currentX + nextX) / 2],
          y: [currentItem.totalValue + (currentItem.totalValue * 0.05)], // Slightly above the line
          text: [`${reduction}% Reduktion`],
          textfont: {
            size: 10,
            color: 'black'
          },
          showlegend: false
        });
      }
    }
    
    // Create annotations for arrows (need to be in the layout)
    const arrowAnnotations: any[] = [];
    
    // Add vertical arrows for consecutive bars
    for (let i = 0; i < topChartData.length - 1; i++) {
      const currentItem = topChartData[i];
      const nextItem = topChartData[i + 1];
      
      if (!config.includeEndOfLife.value || 
          currentItem.withoutEolValue === undefined || 
          nextItem.withoutEolValue === undefined) continue;
      
      const currentX = xValues[i];
      const nextX = xValues[i + 1];
      const shadowOffset = 0.08; // Small offset to create shadow effect
      
      // Arrow from current withoutEol horizontal line to next value
      arrowAnnotations.push({
        x: nextX,                        // End X position (arrow point)
        y: nextItem.withoutEolValue,     // End Y position (arrow point)
        xref: 'x',
        yref: 'y',
        text: '',
        showarrow: true,
        axref: 'x',
        ayref: 'y',
        ax: nextX,                       // Start X position
        ay: currentItem.withoutEolValue, // Start Y position
        arrowhead: 4,                    // Arrowhead style (filled triangle)
        arrowsize: 1.2,                  // Slightly larger arrow
        arrowwidth: 1.5,                 // Slightly thicker arrow
        arrowcolor: 'black'
      });
      
      // Add dashed arrow for total value
      arrowAnnotations.push({
        x: nextX - shadowOffset,         // End X position (arrow point)
        y: nextItem.totalValue,          // End Y position (arrow point)
        xref: 'x',
        yref: 'y',
        text: '',
        showarrow: true,
        axref: 'x',
        ayref: 'y',
        ax: nextX - shadowOffset,        // Start X position
        ay: currentItem.totalValue,      // Start Y position
        arrowhead: 4,                    // Arrowhead style (filled triangle)
        arrowsize: 1.2,                  // Slightly larger arrow
        arrowwidth: 1.5,                 // Slightly thicker arrow
        arrowcolor: 'gray'
      });
    }
    
    // Add vertical disposal arrows for each bar
    if (config.includeEndOfLife.value) {
      topChartData.forEach((item, index) => {
        if (item.withoutEolValue === undefined) return;
        
        const shadowOffset = 0.08;
        const xPos = xValues[index];
        
        // Arrow from withoutEol to total value (pointing upward)
        arrowAnnotations.push({
          x: xPos - shadowOffset,     // End X position
          y: item.totalValue,          // End Y position (arrow point) - Top
          xref: 'x',
          yref: 'y',
          text: '',
          showarrow: true,
          axref: 'x',
          ayref: 'y',
          ax: xPos - shadowOffset,                    // Start X position
          ay: item.withoutEolValue,    // Start Y position - Bottom
          arrowhead: 4,                // Arrowhead style (filled triangle)
          arrowsize: 1.2,              // Slightly larger arrow
          arrowwidth: 1.5,             // Slightly thicker arrow
          arrowcolor: 'gray'
        });
      });
    }
    
    // Prepare the layout for Plotly
    const layout = {
      title: `${totalColumn.label} Comparison - Top 4 Products (Without Disposal)`,
      xaxis: { 
        showticklabels: true,
        tickmode: 'array',
        tickvals: xValues,
        ticktext: topChartData.map(item => item.product),
        tickangle: 0,  // Horizontal text alignment
        hoverformat: '%{text}',
        hoverinfo: 'text',
        hovertext: topChartData.map(item => item.fullProductName),
      },
      yaxis: { 
        title: totalColumn.label, // No units, just the indicator name
        zeroline: true
      },
      barmode: 'group', // Use group mode - overlay won't work for offset bars
      bargap: 0.8,      // Space between groups
      bargroupgap: 0,   // No gap between bars in a group
      legend: { 
        orientation: 'h',
        y: 1.1,         // Position legend above the plot
        xanchor: 'center',
        x: 0.5
      },
      annotations: arrowAnnotations,
      margin: {         // Add more margin at the top for the legend
        t: 80,
        b: 50,
        l: 60,
        r: 50
      }
    };
    
    // Render the plot
    if (graphContainer.value) {
      (window as any).Plotly.newPlot(graphContainer.value, traces, layout);
    }
  };

  return {
    generateLifeCycleComparisonChart
  };
}