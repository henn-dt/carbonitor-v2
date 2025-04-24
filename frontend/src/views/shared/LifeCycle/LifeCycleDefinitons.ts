// frontend/src/views/shared/LifeCycle/LifeCycleDefinitons.ts

import type { ColumnDefinition } from "@/views/shared/ColumnSelector/ColumnDefinition";

// Define the fixed lyfecycles that will always be shown
export const lifeCycleStages: ColumnDefinition[] = [
    { key: 'Production', label: 'Production', default: true, visible: false , tooltip: 'A1-A3 (Production)'},
    { key: 'Construction', label: 'Construction', default: false, visible: false , tooltip: 'A4 (Transport) \n A5 (Assembly)' },
    { key: 'Operation', label: 'Use', default: false, visible: false , tooltip: 'B1-B5 (Use, Maintenance \n and Replacement) '   },
    { key: 'Disassembly', label: 'Demolition', default: false, visible: false , tooltip: 'C1 (Disassembly \nC2 (Transport) ' },
    { key: 'Disposal', label: 'Disposal', default: false, visible: false , tooltip: 'C3 (Waste Processing) \nC4 Disposal)' },
    { key: 'Reuse', label: 'Reuse', default: false, visible: false , tooltip: 'D (Recycling Potential)' },
];


export function getDefaultLifeCycleStages(): ColumnDefinition[] {
    return lifeCycleStages.filter(col => col.default);
}


export const lifecycleColors : Record<string, string> = {
    'Production': '#f8ae5c',    // light orange
    'Construction': '#99d4d8',  // light blue
    'Operation': '#8b98b6',     // greyish blue
    'Disassembly': '#ad9fd9',   // light Purple
    'Disposal': '#71797e',      // Grey
    'Reuse': '#fee0bf',         // Cream
    // Fallback color for any undefined phases
    'default': '#999999'        // Grey
  };


// Helper function to get color for a phase
export function getLifecycleColor(phase: string): string {
    return lifecycleColors[phase] || lifecycleColors.default;
  }
  
  // Helper function to get a lighter version of a color
  export function getLighterColor(baseColor: string, lightenAmount: number = 20): string {
    // Convert hex to HSL, lighten, then back to hex
    // Simple implementation - for production code, use a library like tinycolor2
    
    // Parse hex
    let r = parseInt(baseColor.slice(1, 3), 16);
    let g = parseInt(baseColor.slice(3, 5), 16);
    let b = parseInt(baseColor.slice(5, 7), 16);
    
    // Lighten
    r = Math.min(255, r + lightenAmount);
    g = Math.min(255, g + lightenAmount);
    b = Math.min(255, b + lightenAmount);
    
    // Convert back to hex
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
  }