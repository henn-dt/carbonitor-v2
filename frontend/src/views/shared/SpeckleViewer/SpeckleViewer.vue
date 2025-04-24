<!-- frontend/src/views/shared/SpeckleViewer/SpeckleViewer.vue -->
<template>
  <div class="speckle-viewer-container" ref="viewerContainer" style="position:relative;">
    <!-- The `:key` triggers a remount when isViewerReady becomes true -->
    <slot
      v-if="!loading && !loadError && readyViewer"
      name="controls"
      :viewer="readyViewer"
      :key="readyViewer"
    ></slot>
  </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted, onBeforeUnmount, type PropType, computed , markRaw, type Raw, watch} from 'vue';
  import {
    Viewer,
    DefaultViewerParams,
    SpeckleLoader,
    UrlHelper,
    ViewerEvent
  } from '@speckle/viewer';
  import { CameraController, SelectionExtension , FilteringExtension} from '@speckle/viewer';
  import { getCollectionNodeIdsByNames } from './Selection/getCollections';
  
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
      },
      selectedCollections: {
        type: Array as PropType<String[]>,
        default: () => []
      }
    },
    setup(props, {expose} ) {
        const viewerContainer = ref<HTMLElement | null>(null);
        const loadError = ref<string | null>(null);
        const loading = ref(true);
        
        const isViewerReady = ref<Boolean>(false)
        const viewer = ref<any>(null)
        const readyViewer = computed(() => (isViewerReady.value ? viewer.value : null))
        const renderKey = ref(0);

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
        viewer.value = markRaw(new Viewer(viewerContainer.value, params));        
        await viewer.value.init();
        console.log('ASSIGNING VIEWER', viewer.value)
        isViewerReady.value = true
        renderKey.value = Date.now(); // or increment

        console.log('viewer initialised')
        
        // 4. Add extensions
        const { CameraController, SelectionExtension , FilteringExtension} = speckleModule;
        viewer.value.createExtension(CameraController);
        viewer.value.createExtension(SelectionExtension);
        viewer.value.createExtension(FilteringExtension)
        
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
            viewer.value.getWorldTree(),
            resourceUrl,
            token || '', // Auth token (optional)
            true  // Enable caching
          );
          
          // Load the object
          await viewer.value.loadObject(loader, true);
        }
        
        console.log('Speckle model loaded successfully');
        loading.value = false;
      } catch (error) {
        console.error('Failed to initialize Speckle viewer:', error);
        loadError.value = error instanceof Error ? error.message : String(error);
        loading.value = false;
      }
    };

    watch(
        () => props.selectedCollections,
        (newVal) => {
          if (!viewer.value) return;
          if (newVal && newVal.length > 0) {
            const collectionIds = getCollectionNodeIdsByNames(viewer.value, newVal);
            if (!collectionIds.length) {
              // Optionally clear selection if no matches
              const selection = viewer.value.getExtension(SelectionExtension)
              if (selection) selection.clearSelection();
              return;
            }
            // Select them
            const selection = viewer.value.getExtension(SelectionExtension)
            if (selection) {
              // clear previous if needed
              selection.clearSelection();
              selection.selectObjects(collectionIds);
            }
          } else {
            // Deselect all if passed-in array is empty
            const selection = viewer.value.getExtension(SelectionExtension)
            if (selection) selection.clearSelection();
          }
        }
)
  
      onMounted(() => {
        initViewer();
      });
  
      onBeforeUnmount(() => {
        if (viewer.value) {
          viewer.value.dispose();
          viewer.value = null;
        }
      });

      expose({ readyViewer })

      return {
      viewerContainer,
      loadError,
      loading,
      viewer,
      readyViewer,
      };
    }
  });
  </script>
  
  <style scoped>
  .speckle-viewer-container {
    width: 100%;
    max-height: 100%;
    min-height: 320px;
    min-width: 200px;
    flex: 1
  }
  </style>