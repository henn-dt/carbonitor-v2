import type { Ref } from 'vue';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import { useChartConfiguration } from './useChartConfiguration';

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
  // Get dynamic chart configuration based on number of items
  const { getChartConfig } = useChartConfiguration({
    value: props.selectedIndices
  } as Ref<number[]>);

  const generateLifeCycleComparisonChart = () => {
    // Get dynamic chart configuration
    const chartConfig = getChartConfig();
    
    // Define shadow offset for consistent use throughout
    const shadowOffset = chartConfig.shadowOffset;
    
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
                
        const chartItem: {
          product: string;
          fullProductName: string;
          totalValue: number;
          withoutEolValue?: number;
          rowId: number;
        } = {
          product: fullProductName, // Don't truncate here, will handle dynamically
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
    const xStep = chartConfig.xStep;
    const xValues = topChartData.map((_, i) => xBase + i * xStep);
    
    // Truncate product names based on configuration
    // Use the bar width to determine character limit - wider bars get more characters
    for (let i = 0; i < topChartData.length; i++) {
      const item = topChartData[i];
      let truncateLength = chartConfig.labelTruncateLength;
      
      if (topChartData.length <= 2) {
        // For 1-2 bars, allow more characters
        truncateLength = Math.floor(chartConfig.barWidth * chartConfig.charsPerBarWidth);
      } else if (topChartData.length === 3) {
        // For 3 bars, medium number of characters
        truncateLength = Math.floor(chartConfig.barWidth * chartConfig.charsPerBarWidth * 0.8);
      } else {
        // For 4 bars, fewest characters
        truncateLength = Math.floor(chartConfig.barWidth * chartConfig.charsPerBarWidth * 0.6);
      }
      
      // Apply truncation
      if (item.fullProductName.length > truncateLength) {
        item.product = item.fullProductName.substring(0, truncateLength) + '...';
      }
    }
    
    // Prepare the traces for Plotly
    const traces: any[] = [];
    
    if (config.includeEndOfLife.value) {
      // First add the total value as a gray bar (shadow effect)
      // Shift it to the left for better separation (25% of bar width)
      traces.push({
        type: 'bar',
        x: xValues.map(x => x - shadowOffset), // Offset to the left by 25% of bar width
        y: topChartData.map(item => item.totalValue),
        width: chartConfig.barWidth,
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
        width: chartConfig.barWidth,
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
        // Remove text near bars
        textposition: 'none'
      });
      
      // For each bar, add the vertical cutted line with arrow (but no text)
      // Only for the highest bar (first after sorting)
      if (topChartData.length > 0) {
        const highestItem = topChartData[0];
        if (highestItem.withoutEolValue !== undefined) {
          const xPos = xValues[0]; // Position of the highest bar
          // Calculate exact center of gray portion - perfect alignment with arrow
          const grayBarCenter = xPos - (shadowOffset / 2);
          
          // Do not add separate line since it will be included in the arrow
          // The arrow itself will act as the vertical line
        }
      }
      
      // Create cascade comparison from highest bar to each subsequent bar
      if (topChartData.length > 1) {
        // Find indices after sorting
        const highestBarIndex = 0; // After sorting, the highest is always the first
        const highestItem = topChartData[highestBarIndex];
        const highestX = xValues[highestBarIndex];

        // Process each bar after the highest one
        for (let i = 1; i < topChartData.length; i++) {
          const currentItem = topChartData[i];
          const currentX = xValues[i];
          
          if (currentItem.withoutEolValue === undefined || highestItem.withoutEolValue === undefined) continue;
          
          // For the second bar (i=1), draw lines directly from highest bar
          if (i === 1) {
            // Add dashed horizontal line from highest total to current total (with disposal)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [highestX - shadowOffset, currentX - shadowOffset], 
              y: [highestItem.totalValue, highestItem.totalValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'gray',
                dash: 'dash'  // Make the line dashed
              },
              showlegend: false
            });
            
            // Add solid horizontal line from highest withoutEol to current withoutEol (with dash)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [highestX, currentX], 
              y: [highestItem.withoutEolValue, highestItem.withoutEolValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'black',
                dash: 'dash' // Make the black line dashed too
              },
              showlegend: false
            });
          } 
          // For third and subsequent bars (i>=2), branch from the previous bar's position on the main line
          else {
            const previousX = xValues[i-1];
            
            // Add dashed branch line from main horizontal line to current bar (total value)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [previousX - shadowOffset, currentX - shadowOffset], 
              y: [highestItem.totalValue, highestItem.totalValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'gray',
                dash: 'dash'
              },
              showlegend: false
            });
            
            // Add solid branch line from main horizontal line to current bar (without EOL, with dash)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [previousX, currentX], 
              y: [highestItem.withoutEolValue, highestItem.withoutEolValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'black',
                dash: 'dash' // Make the black line dashed too
              },
              showlegend: false
            });
          }
        }
      }
    } else {
      // Just show single bars without EndOfLife comparison
      traces.push({
        type: 'bar',
        x: xValues,
        y: topChartData.map(item => item.totalValue),
        width: chartConfig.barWidth,
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
        // Remove text near bars
        textposition: 'none'
      });
      
      // Create cascade comparison from highest bar to each subsequent bar
      if (topChartData.length > 1) {
        // Find indices after sorting
        const highestBarIndex = 0; // After sorting, the highest is always the first
        const highestItem = topChartData[highestBarIndex];
        const highestX = xValues[highestBarIndex];

        // Process each bar after the highest one
        for (let i = 1; i < topChartData.length; i++) {
          const currentItem = topChartData[i];
          const currentX = xValues[i];
          
          // For the second bar (i=1), draw lines directly from highest bar
          if (i === 1) {
            // Add horizontal line from highest to current (with dash)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [highestX, currentX],
              y: [highestItem.totalValue, highestItem.totalValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'black',
                dash: 'dash' // Make the black line dashed
              },
              showlegend: false
            });
          } 
          // For third and subsequent bars (i>=2), branch from the previous bar's position on the main line
          else {
            const previousX = xValues[i-1];
            
            // Add branch line from main horizontal line to current bar (with dash)
            traces.push({
              type: 'scatter',
              mode: 'lines',
              x: [previousX, currentX],
              y: [highestItem.totalValue, highestItem.totalValue],
              line: {
                width: chartConfig.lineWidth,
                color: 'black',
                dash: 'dash' // Make the black line dashed
              },
              showlegend: false
            });
          }
        }
      }
    }
    
    // Create annotations for arrows and text (better placement control)
    const arrowAnnotations: any[] = [];
    
    // Add vertical arrows for comparison to highest bar (only for EOL comparisons)
    if (config.includeEndOfLife.value && topChartData.length > 1) {
      const highestItem = topChartData[0]; // Highest bar (first after sorting)
      
      // For each bar after the highest
      for (let i = 1; i < topChartData.length; i++) {
        const currentItem = topChartData[i];
        
        if (currentItem.withoutEolValue === undefined || highestItem.withoutEolValue === undefined) continue;
        
        const currentX = xValues[i];
        
        // Calculate reduction percentages compared to highest bar
        const totalReduction = ((highestItem.totalValue - currentItem.totalValue) / highestItem.totalValue * 100).toFixed(1);
        const withoutEolReduction = ((highestItem.withoutEolValue - currentItem.withoutEolValue) / highestItem.withoutEolValue * 100).toFixed(1);
        
        // Add text directly in layout annotations with white background boxes - aligned with arrows
        arrowAnnotations.push({
          x: currentX - 0.3, // Position closer to the arrow
          y: (highestItem.totalValue + currentItem.totalValue) / 2, // Position at midpoint of arrow
          text: `${totalReduction}% Total Reduktion`,
          showarrow: false,
          font: {
            size: chartConfig.lineLabelFontSize,
            color: 'gray'
          },
          xanchor: 'right', // Right align text so it extends away from the bar
          yanchor: 'middle', // Middle align vertically to center with arrow
          bgcolor: 'white', // White background
          bordercolor: '#d3d3d3', // Light gray border
          borderpad: 4, // Padding inside the box
          borderwidth: 1, // Border width
          opacity: 0.9, // Slight transparency
          boxshadow: true // Add shadow to box
        });
        
        // GWP reduction text - aligned with arrows
        arrowAnnotations.push({
          x: currentX - 0.3, // Position closer to the arrow
          y: (highestItem.withoutEolValue + currentItem.withoutEolValue) / 2, // Position at midpoint of arrow
          text: `${withoutEolReduction}% ${indicatorKey}-Reduktion`,
          showarrow: false,
          font: {
            size: chartConfig.lineLabelFontSize,
            color: 'black'
          },
          xanchor: 'right', // Right align text so it extends away from the bar
          yanchor: 'middle', // Middle align vertically to center with arrow
          bgcolor: 'white', // White background
          bordercolor: '#d3d3d3', // Light gray border
          borderpad: 4, // Padding inside the box
          borderwidth: 1, // Border width
          opacity: 0.9, // Slight transparency
          boxshadow: true // Add shadow to box
        });
        
        // Arrow from highest withoutEol horizontal line to current value
        arrowAnnotations.push({
          x: currentX,                        // End X position (arrow point)
          y: currentItem.withoutEolValue,     // End Y position (arrow point)
          xref: 'x',
          yref: 'y',
          text: '',
          showarrow: true,
          axref: 'x',
          ayref: 'y',
          ax: currentX,                       // Start X position
          ay: highestItem.withoutEolValue,    // Start Y position
          arrowhead: 4,                       // Arrowhead style (filled triangle)
          arrowsize: chartConfig.arrowSize,   // Adjusted arrow size
          arrowwidth: chartConfig.arrowWidth, // Adjusted arrow width
          arrowcolor: 'black',
          line: {
            dash: 'dash'                      // Make the line dashed
          }
        });
        
        // Calculate the exact coordinates for the gray bar
        const grayBarXCenter = currentX - shadowOffset; // Center of gray portion
        const grayBarTopY = currentItem.totalValue; // Top edge of gray bar
        
        // Add a dot at the exact center of the top edge of gray bar for precision
        arrowAnnotations.push({
          x: grayBarXCenter,             // Center of gray portion
          y: grayBarTopY,                // Top edge of gray bar
          xref: 'x',
          yref: 'y',
          text: '',
          showarrow: true,
          axref: 'x',
          ayref: 'y',
          ax: grayBarXCenter,            // Same X position (vertical line)
          ay: highestItem.totalValue,    // Start from highest bar's top edge
          arrowhead: 4,                  // Arrowhead style
          arrowsize: chartConfig.arrowSize,
          arrowwidth: chartConfig.arrowWidth,
          arrowcolor: 'gray',
          line: {
            dash: 'dash'
          }
        });
      }
    }
    
    // Add vertical arrows for comparison to highest bar (only for non-EOL comparisons)
    if (!config.includeEndOfLife.value && topChartData.length > 1) {
      const highestItem = topChartData[0]; // Highest bar (first after sorting)
      
      // For each bar after the highest
      for (let i = 1; i < topChartData.length; i++) {
        const currentItem = topChartData[i];
        const currentX = xValues[i];
        
        // Calculate reduction percentage compared to highest bar
        const reduction = ((highestItem.totalValue - currentItem.totalValue) / highestItem.totalValue * 100).toFixed(1);
        
        // Add reduction text with white background box - aligned with arrow
        arrowAnnotations.push({
          x: currentX - 0.3, // Position closer to the arrow
          y: (highestItem.totalValue + currentItem.totalValue) / 2, // Position at midpoint of arrow
          text: `${reduction}% Reduktion`,
          showarrow: false,
          font: {
            size: chartConfig.lineLabelFontSize,
            color: 'black'
          },
          xanchor: 'right', // Right align text so it extends away from the bar
          yanchor: 'middle', // Middle align vertically to center with arrow
          bgcolor: 'white', // White background
          bordercolor: '#d3d3d3', // Light gray border
          borderpad: 4, // Padding inside the box
          borderwidth: 1, // Border width
          opacity: 0.9, // Slight transparency
          boxshadow: true // Add shadow to box
        });
        
        // Arrow from highest horizontal line to current value
        arrowAnnotations.push({
          x: currentX,                   // End X position (arrow point)
          y: currentItem.totalValue,     // End Y position (arrow point)
          xref: 'x',
          yref: 'y',
          text: '',
          showarrow: true,
          axref: 'x',
          ayref: 'y',
          ax: currentX,                  // Start X position
          ay: highestItem.totalValue,    // Start Y position
          arrowhead: 4,                  // Arrowhead style (filled triangle)
          arrowsize: chartConfig.arrowSize,      // Adjusted arrow size
          arrowwidth: chartConfig.arrowWidth,    // Adjusted arrow width
          arrowcolor: 'black',
          line: {
            dash: 'dash'                 // Make the line dashed
          }
        });
      }
    }
    
    // Add vertical arrow for the first/highest bar - with exact position on gray bar
    if (config.includeEndOfLife.value && topChartData.length > 0) {
      // Only add for the highest bar (first after sorting)
      const highestItem = topChartData[0];
      
      if (highestItem.withoutEolValue !== undefined) {
        const xPos = xValues[0]; // Position of the highest bar
        // Calculate exact center of gray portion horizontally
        const grayBarCenter = xPos - shadowOffset;
        
        // Get exact Y coordinates of the gray bar
        const grayBarTopY = highestItem.totalValue;
        const grayBarBottomY = highestItem.withoutEolValue;
        
        // Place arrow from bottom to top of the gray portion, exactly in the center
        arrowAnnotations.push({
          x: grayBarCenter,              // End X position (center of gray portion)
          y: grayBarTopY,                // Exact top edge of gray bar
          xref: 'x',
          yref: 'y',
          text: '',
          showarrow: true,
          axref: 'x',
          ayref: 'y',
          ax: grayBarCenter,             // Same X position for vertical line
          ay: grayBarBottomY,            // Exact bottom edge of gray bar
          arrowhead: 4,                  // Arrowhead style
          arrowsize: chartConfig.arrowSize,
          arrowwidth: chartConfig.arrowWidth,
          arrowcolor: 'gray',
          line: {
            dash: 'dash'
          }
        });
      }
    }
    
    // Prepare the layout for Plotly
    const layout = {
      title: `${indicatorKey.toUpperCase()} Comparison - Top ${topChartData.length} Products`,
      xaxis: { 
        showticklabels: true,
        tickmode: 'array',
        tickvals: xValues,
        ticktext: topChartData.map(item => item.product),
        tickangle: 0,  // Horizontal text alignment
        hoverformat: '%{text}',
        hoverinfo: 'text',
        hovertext: topChartData.map(item => item.fullProductName),
        // Add more margin on x-axis to ensure text is visible
        range: [
          xBase - chartConfig.barWidth - 1.5, // Minimum value with extra margin
          xValues[xValues.length - 1] + chartConfig.barWidth + 1.5 // Maximum value with extra margin
        ]
      },
      yaxis: { 
        title: totalColumn.label, // No units, just the indicator name
        zeroline: true,
        // Add bottom margin to ensure text below bars is visible
        rangemode: 'tozero',
        automargin: true
      },
      barmode: 'group', // Use group mode - overlay won't work for offset bars
      bargap: chartConfig.barGap,      // Space between groups (dynamically set)
      bargroupgap: chartConfig.barGroupGap,   // Gap between bars in a group (dynamically set)
      legend: { 
        orientation: 'h',
        y: 1.1,         // Position legend above the plot
        xanchor: 'center',
        x: 0.5
      },
      annotations: arrowAnnotations,
      margin: {         // Add more margin at the top for the legend and bottom for text
        t: 80,
        b: 100,  // Increased bottom margin
        l: 100,  // Increased left margin
        r: 80    // Increased right margin
      },
      // Adjust plot area to fit number of bars better
      width: topChartData.length <= 2 ? 900 : (topChartData.length === 3 ? 1000 : 1100),
      height: 600,
      autosize: false
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