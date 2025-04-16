<template>
    <div class="speckle-viewer-container" ref="viewerContainer"></div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, onBeforeUnmount, type PropType } from 'vue';
  import {
    Viewer,
    DefaultViewerParams,
    SpeckleLoader,
    UrlHelper,
    ViewerEvent
  } from '@speckle/viewer';
  import { CameraController, SelectionExtension } from '@speckle/viewer';
  
  export interface SpeckleModelData {
    modelUrl: string;
    modelMapping?: string;
    token? : string;
  }
  
  export default defineComponent({
    name: 'SpeckleViewer',
    props: {
      modelData: {
        type: Object as PropType<SpeckleModelData>,
        required: true
      }
    },
    setup(props) {
        const viewerContainer = ref<HTMLElement | null>(null);
        const loadError = ref<string | null>(null);
        const loading = ref(true);
        let viewer: any = null;



    const getSpeckleToken = async () => {
      // First priority: Token provided directly in props
      if (props.modelData.token) {
        return props.modelData.token;
      }

      // Second priority: Token from environment variables
      if (import.meta.env.VITE_SPECKLE_TOKEN) {
        console.log('Using Speckle token from environment variables');
        return import.meta.env.VITE_SPECKLE_TOKEN;
      }
    };
  
    const initViewer = async () => {
        if (!viewerContainer.value) return;
  
        try {
        loading.value = true;
        loadError.value = null;
        
        // 1. Import Speckle viewer
        const speckleModule = await import('@speckle/viewer');
        const { Viewer, DefaultViewerParams, SpeckleLoader, ViewerEvent } = speckleModule;
        
        // 2. Configure viewer
        const params = DefaultViewerParams;
        params.verbose = true;
        
        // 3. Create and initialize viewer
        viewer = new Viewer(viewerContainer.value, params);
        await viewer.init();
        
        // 4. Add extensions
        const { CameraController, SelectionExtension } = speckleModule;
        viewer.createExtension(CameraController);
        viewer.createExtension(SelectionExtension);
        
        // 5. Get authentication token
        const token = await getSpeckleToken();
        
        // 5. Use UrlHelper to get the correct resource URLs
        console.log(`Resolving Speckle model URL: ${props.modelData.modelUrl}`);
        
        // Let UrlHelper handle the URL parsing and formatting
        const resourceUrls = await UrlHelper.getResourceUrls(props.modelData.modelUrl);
        
        if (!resourceUrls || resourceUrls.length === 0) {
          throw new Error('Could not resolve any resource URLs for the provided model URL');
        }
        
        console.log(`Resolved ${resourceUrls.length} resource URLs`);
        
        // 6. Load each resource URL
        for (const resourceUrl of resourceUrls) {
          console.log(`Loading resource from: ${resourceUrl}`);
          
          // Create the SpeckleLoader with the correct parameters
          const loader = new SpeckleLoader(
            viewer.getWorldTree(),
            resourceUrl,
            token || '', // Auth token (optional)
            true  // Enable caching
          );
          
          // Load the object
          await viewer.loadObject(loader, true);
        }
        
        console.log('Speckle model loaded successfully');
        loading.value = false;
      } catch (error) {
        console.error('Failed to initialize Speckle viewer:', error);
        loadError.value = error instanceof Error ? error.message : String(error);
        loading.value = false;
      }
    };
  
      onMounted(() => {
        initViewer();
      });
  
      onBeforeUnmount(() => {
        if (viewer) {
          viewer.dispose();
          viewer = null;
        }
      });
  
      return {
    viewerContainer,
      loadError,
      loading
      };
    }
  });
  </script>
  
  <style scoped>
  .speckle-viewer-container {
    width: 100%;
    height: 100%;
    min-height: 400px;
  }
  </style>