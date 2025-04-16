//frontend/src/composables/createRefreshableService.ts

import { useRefreshableService } from '@/composables/useRefreshableService';


export function createRefreshableService<T extends object>(
    serviceInstance: T,
    methodNames: (keyof T & string)[],
    options = { refreshInterval: 5 * 60 * 1000 }
  ): T & { 
    startAllBackgroundRefreshes: () => void;
    stopAllBackgroundRefreshes: () => void;
  } {

    
    // Create refreshable versions of each method
    const refreshables = methodNames.reduce((acc, methodName) => {
      if (typeof serviceInstance[methodName] === 'function') {
        acc[methodName] = useRefreshableService(
          serviceInstance[methodName].bind(serviceInstance),
          options
        );
      }
      return acc;
    }, {} as Record<string, ReturnType<typeof useRefreshableService>>);
    
    // Create proxy service that enhances the original service
    const enhancedService = new Proxy(serviceInstance, {
      get(target, prop: string | symbol) {
        const propName = prop.toString();
        
        // If it's one of our refreshable methods
        if (refreshables[propName]) {
          return refreshables[propName].refreshableFetch;
        }
        
        // Otherwise return the original method or property
        return target[prop as keyof T];
      }
    });
  
    // Add helper methods to start/stop all background refreshes
    const startAllBackgroundRefreshes = () => {
      Object.values(refreshables).forEach(refreshable => refreshable.startBackgroundRefresh());
    };
  
    const stopAllBackgroundRefreshes = () => {
      Object.values(refreshables).forEach(refreshable => refreshable.stopBackgroundRefresh());
    };
  
    return Object.assign(enhancedService, {
      startAllBackgroundRefreshes,
      stopAllBackgroundRefreshes
    });
  }