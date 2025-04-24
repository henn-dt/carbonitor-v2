import type { Ref } from 'vue';

// Configuration interface for chart settings
export interface ChartConfig {
  // Bar settings
  barWidth: number;
  barGroupGap: number;
  barGap: number;
  
  // Text settings
  labelTruncateLength: number;
  lineLabelFontSize: number;
  disposalLabelFontSize: number;
  
  // Position settings
  xStep: number;
  shadowOffset: number;
  
  // Line settings
  lineWidth: number;
  arrowSize: number;
  arrowWidth: number;
  
  // Label adjustment
  charsPerBarWidth: number; // How many characters per bar width unit
}

export function useChartConfiguration(selectedIndices: Ref<number[]>) {
  /**
   * Get dynamic chart configuration based on number of items
   */
  const getChartConfig = (): ChartConfig => {
    // Get number of bars to display (limited to max 4)
    const numBars = Math.min(selectedIndices.value.length, 4);
    
    // Base configuration options
    let config: ChartConfig = {
      barWidth: 0.8,               // Wider base bar width
      barGroupGap: 0,
      barGap: 0.7,
      labelTruncateLength: 20,
      lineLabelFontSize: 10,
      disposalLabelFontSize: 9,
      xStep: 3.5,                  // More space between bars by default
      shadowOffset: 0.25 * 0.8,    // 25% of the bar width (0.8 is default bar width)
      lineWidth: 1.2,              // Thicker line width for better visibility of dashes
      arrowSize: 1.2,
      arrowWidth: 1.5,
      charsPerBarWidth: 40         // Base ratio of chars to bar width
    };
    
    // Adjust configuration based on number of bars
    if (numBars === 1) {
      // For single bar, center it and make it wider
      config.barWidth = 1.2;
      config.xStep = 0; // Not used with single bar
      config.lineLabelFontSize = 12;
      config.disposalLabelFontSize = 11;
      config.barGap = 0;
      config.arrowSize = 1.5;
      config.arrowWidth = 2.0;
      config.labelTruncateLength = 40;
    }
    else if (numBars === 2) {
      // For 2 bars, make them wider with adequate spacing
      config.barWidth = 1.1;         
      config.xStep = 4.0;              
      config.lineLabelFontSize = 12; 
      config.disposalLabelFontSize = 11;
      config.barGap = 0.5;         
      config.arrowSize = 1.5;        
      config.arrowWidth = 1.8;      
      config.labelTruncateLength = 36;
    } else if (numBars === 3) {
      // For 3 bars, use medium sizing but adequate spacing
      config.barWidth = 1.0;
      config.xStep = 3.5;           
      config.lineLabelFontSize = 11;
      config.disposalLabelFontSize = 10;
      config.barGap = 0.6;
      config.arrowSize = 1.4;
      config.arrowWidth = 1.7;
      config.labelTruncateLength = 30;
    } else {
      // For 4 bars, still use reasonable sizing
      config.barWidth = 0.8;
      config.xStep = 3.0;
      config.lineLabelFontSize = 10;
      config.labelTruncateLength = 24;
    }
    
    return config;
  };
  
  return {
    getChartConfig
  };
}