// frontend/src/stores/colorStore.ts
import { defineStore } from 'pinia';
import chroma from 'chroma-js'


export const useColorStore = defineStore('color', {
  state: () => ({
    productMappingColor: {} as Record<string, string>,
    lifeCycleColors : LIFECYCLE_COLORS,
    themeColors: DATA_COLORS
  }),
  actions: {
    setProductMappingsColors(mappings: string[]) {
      const n = mappings.length;
      const mappingsPalette = n <= palette.length
        ? palette.slice(0, n)
        : chroma.scale(palette).mode('lab').colors(n);
      this.productMappingColor = {};
      mappings.forEach((cat, i) => this.productMappingColor[cat] = mappingsPalette[i]);
    },
    // method to force-set or override a particular mapping
    setProductMappingColor(mapping: string, color: string) {
      this.productMappingColor[mapping] = color;
    }
  },
  getters: {
    // Use as: colorStore.heatmapScale(value)
    heatmapScale: () => chroma.scale(['#1d5d32', '#91c7ad', '#ffffff', '#ef4d04']).mode('lab'),    // green to light green to white to red
    divergentScale: () => chroma.scale(['#00eaff', '#ff4deb']).mode('lab'),    // cyan to magenta
    nThemeColors: () => (n: number) => chroma.scale(palette).mode('lab').colors(n),   // returns function to get n colors in the theme´s color space
    getLifecycleColor: (state) => (phase: string): string =>
      state.lifeCycleColors[phase] || state.lifeCycleColors.default,
    // Optionally: get a *lighter* phase color, using chroma for robustness
    getLighterLifecycleColor: (state) => (phase: string, lightenAmount: number = 0.4): string => {
      const base = state.lifeCycleColors[phase] || state.lifeCycleColors.default
      try {
        return chroma(base).brighten(lightenAmount).hex()
      } catch {
        return base // fallback if color is invalid
      }
    }
  }
});


const LIFECYCLE_COLORS : Record<string, string> = {
  'Production': '#f8ae5c',    // light orange
  'Construction': '#99d4d8',  // light blue
  'Operation': '#8b98b6',     // greyish blue
  'Disassembly': '#ad9fd9',   // light Purple
  'Disposal': '#71797e',      // Grey
  'Reuse': '#fee0bf',         // Cream
  // Fallback color for any undefined phases
  'default': '#999999'        // Grey
};

const DATA_COLORS : Record<string, string> = {
  'color_0' : '#70e5b6',    // fresh mint green (cheerful, compliments main green)
  'color_1' : '#ffb547',    // warm tangerine (lively orange-yellow)
  'color_2' : '#5ecbf3',    // sky blue (bright and friendly)
  'color_3' : '#ffe766',    // sunny yellow (cheerful, not muddy)
  'color_4' : '#ff71a5',    // happy pink (vivid, energetic)
  'color_5' : '#38aade',    // clear blue (distinct from green)
  'color_6' : '#fb6868',    // coral red (lively contrast)
  'color_7' : '#b7ecec',    // light aqua (pale, but not dull)
  'color_8' : '#ffabfa',    // playful lavender-pink
  'color_9' : '#b890ee'     // crisp lilac (pastel but not dusty)
}

const DATA_COLORS_DEMURE : Record<string, string> = {
    'color_0' : '#9edee0',    // light green
    'color_1' : '#fe7c62',    // orange
    'color_2' : '#7fd4cf',    // light blue green
    'color_3' : '#e0b63e',    // yellow
    'color_4' : '#df929c',    // pink
    'color_5' : '#318ca6',    // darker blue green
    'color_6' : '#d84d1e',    // darker orange
    'color_7' : '#d9e2e6',    // light blue
    'color_8' : '#d7a928',    // darker yellow
    'color_9' : '#bd85be'     // purple
}

const palette = Object.values(DATA_COLORS)