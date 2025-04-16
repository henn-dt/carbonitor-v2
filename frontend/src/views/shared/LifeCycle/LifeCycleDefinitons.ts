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