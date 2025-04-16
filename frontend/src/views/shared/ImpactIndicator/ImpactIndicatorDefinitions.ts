import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { ImpactCategoryKey } from 'lcax';

// Define the fixed impact categories that will always be shown
export const fixedImpactCategories: ColumnDefinition[] = [
	{ key: 'gwp', label: 'GWP total', default: true, visible: false, tooltip: 'Global \nWarming \nPotential \n (kg CO2 eq.)' },
	{ key: 'gwp_fos', label: 'GWP fossil', default: false, visible: false, tooltip: 'GWP Fossil \n (kg CO2 eq.)' },
	{ key: 'gwp_bio', label: 'GWP biogenic', default: false, visible: false, tooltip: 'GWP Biogenic \n (kg CO2 eq.)' },
	{ key: 'gwp_lul', label: 'GWP Land Use', default: false, visible: false, tooltip: 'GWP Land Use / \n Land Use Change\n (kg CO2 eq.)' },
	{ key: 'fw', label: 'Water Use', default: true, visible: false, tooltip: 'Net use of fresh water\n (m3)' },
];

// Define all impact category columns for the More... selector
// Note: 'fw' (Water Use) is moved to the fixed display but excluded here
export const moreImpactCategoryColumns: ColumnDefinition[] = [
	{ key: 'odp', label: 'ODP', default: false, visible: false, tooltip: 'Ozone Depletion Potential \n (kg CFC-11 eq.)' },
	{ key: 'ap', label: 'AP', default: false, visible: false, tooltip: 'Acidification Potential\n (Mole of H+ eq.)' },
	{ key: 'ep', label: 'EP', default: false, visible: false, tooltip: 'Eutrophication Potential\n (Mole of N eq.)' },
	{ key: 'ep_fw', label: 'EP fw', default: false, visible: false, tooltip: 'Eutrophication Potential - Freshwater \n (kg P eq.)' },
	{ key: 'ep_mar', label: 'EP mar', default: false, visible: false, tooltip: 'Eutrophication Potential - Marine \n (kg N eq.)' },
	{ key: 'ep_ter', label: 'EP ter', default: false, visible: false, tooltip: 'Eutrophication Potential - Terrestrial\n (kg N eq.)' },
	{ key: 'pocp', label: 'POCP', default: false, visible: false, tooltip: 'Photochemical Ozone Creation Potential\n (kg NMVOC eq.)' },
	{ key: 'adpe', label: 'ADPE', default: false, visible: false, tooltip: 'Abiotic Depletion Potential - Elements' }, //?
	{ key: 'adpf', label: 'ADPF', default: false, visible: false, tooltip: 'Abiotic Depletion Potential - Fossil Fuels' }, //?
	{ key: 'penre', label: 'PENRE', default: false, visible: false, tooltip: 'Primary Energy Non-Renewable\n (MJ)' },
	{ key: 'pere', label: 'PERE', default: false, visible: false, tooltip: 'Primary Energy Renewable \n (MJ)' },
	{ key: 'perm', label: 'PERM', default: false, visible: false, tooltip: 'Primary Energy Renewable - Material \n (MJ)'  },
	{ key: 'pert', label: 'PERT', default: false, visible: false, tooltip: 'Primary Energy Renewable - Total \n (MJ)'  },
	{ key: 'penrt', label: 'PENRT', default: false, visible: false, tooltip: 'Primary Energy Non-Renewable - Total \n (MJ)' },
	{ key: 'penrm', label: 'PENRM', default: false, visible: false, tooltip: 'Primary Energy Non-Renewable - Material \n (MJ)' },
	{ key: 'sm', label: 'SM', default: false, visible: false, tooltip: 'Use of secondary material \n (kg)' },
	{ key: 'pm', label: 'PM', default: false, visible: false, tooltip: 'Incidence of disease due to PM emissions' }, //?
	{ key: 'wdp', label: 'WDP', default: false, visible: false, tooltip: 'Water Depletion Potential' },
	{ key: 'irp', label: 'IRP', default: false, visible: false, tooltip: 'Exposure efficiency relative to U235' },
	{ key: 'etp_fw', label: 'ETP fw', default: false, visible: false, tooltip: 'Toxic Unit for ecosystems' },
	{ key: 'htp_c', label: 'HTP c', default: false, visible: false, tooltip: 'Human Toxicity Potential - Carcinogenic' },
	{ key: 'htp_nc', label: 'HTP nc', default: false, visible: false, tooltip: 'Human Toxicity Potential - Non-Carcinogenic' },
	{ key: 'sqp', label: 'SQP', default: false, visible: false, tooltip: 'Soil Quality Potential' },
	{ key: 'rsf', label: 'RSF', default: false, visible: false, tooltip: 'Renewable Secondary Fuels \n (MJ)' },
	{ key: 'nrsf', label: 'NRSF', default: false, visible: false, tooltip: 'Non-Renewable Secondary Fuels \n (MJ)' },
	{ key: 'hwd', label: 'HWD', default: false, visible: false, tooltip: 'Hazardous Waste Disposed \n (kg)' },
	{ key: 'nhwd', label: 'NHWD', default: false, visible: false, tooltip: 'Non-Hazardous Waste Disposed \n (kg)' },
	{ key: 'rwd', label: 'RWD', default: false, visible: false, tooltip: 'Radioactive Waste Disposed \n (kg)' },
	{ key: 'cru', label: 'CRU', default: false, visible: false, tooltip: 'Components for Reuse \n (kg)' },
	{ key: 'mrf', label: 'MRF', default: false, visible: false, tooltip: 'Materials for Recycling \n (kg)' },
	{ key: 'mer', label: 'MER', default: false, visible: false, tooltip: 'Materials for Energy Recovery \n (kg)' },
	{ key: 'eee', label: 'EEE', default: false, visible: false, tooltip: 'Exported Electrical Energy \n (MJ)' },
	{ key: 'eet', label: 'EET', default: false, visible: false, tooltip: 'Exported Thermal Energy \n (MJ)'  }
];

// Helper function to get default impact categories
export function getDefaultImpactCategories(): ColumnDefinition[] {
  // Return only default categories from both fixed and more lists
  return [
    ...fixedImpactCategories.filter(col => col.default),
    ...moreImpactCategoryColumns.filter(col => col.default)
  ];
}

export function getDefaultMoreImpactCategoryColumns(): ColumnDefinition[] {
	return moreImpactCategoryColumns.filter(col => col.default);
}

// Helper function to get all impact categories (fixed + more)
export function getAllImpactCategories(): ColumnDefinition[] {
  return [...fixedImpactCategories, ...moreImpactCategoryColumns];
}

// Helper function to get column definitions for given keys
export function getImpactCategoryDefinitionsByKeys(keys: string[]): ColumnDefinition[] {
  return getAllImpactCategories().filter(col => keys.includes(col.key));
}

// Helper function to convert ColumnDefinition array to keys array
export function getKeysFromImpactCategories(columns: ColumnDefinition[]): ImpactCategoryKey[] {
  return columns.map(col => col.key as ImpactCategoryKey);
}

// Get a human-readable label for an impact category
export function getImpactCategoryLabel(key: ImpactCategoryKey): string {
  const category = getAllImpactCategories().find(col => col.key === key);
  return category ? category.label : key;
}