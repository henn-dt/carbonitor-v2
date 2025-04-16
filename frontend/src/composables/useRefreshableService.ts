// src/composables/useRefreshableService.ts
import { ref } from 'vue';

export interface RefreshableServiceOptions {
  refreshInterval?: number;
  autoStartRefresh?: boolean;
}

export function useRefreshableService<T, F extends (...args: any[]) => Promise<any>>(
  fetchFunction: F,
  options: RefreshableServiceOptions = {}
) {
  const REFRESH_INTERVAL = options.refreshInterval || 5 * 60 * 1000; // Default 5 minutes
  const lastFetch = ref<Date | null>(null);
  let refreshTimer: number | null = null;

  // Wrap the fetch function with refreshing logic
  const refreshableFetch = async (force = false, ...args: Parameters<F>): Promise<ReturnType<F>> => {
    const currentTime = new Date();
    const shouldRefresh = force || 
      !lastFetch.value || 
      (currentTime.getTime() - lastFetch.value.getTime() > REFRESH_INTERVAL);
    
    // Perform the fetch if we should refresh or don't have data yet
    if (shouldRefresh) {
      const result = await fetchFunction(...args);
      lastFetch.value = new Date();
      return result;
    }
    
    // Otherwise, just return the result of calling the function normally
    return fetchFunction(...args);
  };

  // Start background refresh
  const startBackgroundRefresh = (args?: Parameters<F>) => {
    stopBackgroundRefresh();
    
    refreshTimer = window.setInterval(() => {
      refreshableFetch(true, ...(args || [] as any));
    }, REFRESH_INTERVAL);
  };

  // Stop background refresh
  const stopBackgroundRefresh = () => {
    if (refreshTimer) {
      window.clearInterval(refreshTimer);
      refreshTimer = null;
    }
  };

  // Auto-start if configured
  if (options.autoStartRefresh) {
    startBackgroundRefresh();
  }

  return {
    lastFetch,
    refreshableFetch,
    startBackgroundRefresh,
    stopBackgroundRefresh
  };
}