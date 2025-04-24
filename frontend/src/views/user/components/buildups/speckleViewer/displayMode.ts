// frontend/src/views/user/components/buildups/speckleViewer/buildupViewerDisplayMode.ts
import { useColorStore } from "@/stores/colorStore"
import { getCollectionNodeIdsByNames, getCollectionNodeIdsByExcludedNames, getElementIdsUnderCollectionNodes } from "@/views/shared/SpeckleViewer/Selection/getCollections";
import { Viewer, WorldTree, FilteringExtension } from '@speckle/viewer';

export type GraphicMode = 'modelGroups' | 'mappedElements' | 'nonMappedElements' | 'noOverrides'

export async function applyDisplayMode(
    viewer: Viewer,
    mode: GraphicMode,
    colorStore: ReturnType<typeof useColorStore>
  ) {
    if (!viewer || !colorStore) return

    const filtering = viewer.getExtension(FilteringExtension) as FilteringExtension
    if (!filtering) return

    const mappedGroupNames = Object.keys(colorStore.productMappingColor)   // refactor later, to only get the current buildups mapped groups. 

    // collections
    const mappedGroupNodeIds = getCollectionNodeIdsByNames(viewer, mappedGroupNames)
    const nonMappedGroupNodeIds = getCollectionNodeIdsByExcludedNames(viewer, mappedGroupNames)

    // traversal
    const mappedElementIds = getElementIdsUnderCollectionNodes(viewer, mappedGroupNodeIds)
    const nonMappedElementIds = getElementIdsUnderCollectionNodes(viewer, nonMappedGroupNodeIds)
    const allElementIds = mappedElementIds.concat(nonMappedElementIds)


    filtering.resetFilters()
    filtering.removeUserObjectColors()
    filtering.removeColorFilter()

  if (mode === 'modelGroups') {
    // Map each group to a color group [{objectIds, color}]
    const colorGroups: { objectIds: string[]; color: string }[] = []
    for (const group of mappedGroupNames) {
      // Find collection node(s) for this group (protect against missing collections)
      const groupNodeIds = getCollectionNodeIdsByNames(viewer, [group])

      const groupElementIds = getElementIdsUnderCollectionNodes(viewer, groupNodeIds)
      if (groupElementIds.length && colorStore.productMappingColor[group]) {
        colorGroups.push({
          objectIds: groupElementIds,
          color: colorStore.productMappingColor[group]
        })
      }
    }
    // Apply as "user object colors"
    filtering.showObjects(allElementIds)
    if (colorGroups.length) filtering.setUserObjectColors(colorGroups)
    // "Ghost" (= 50% transparent) all non-mapped elements
    if (nonMappedElementIds.length)
      filtering.isolateObjects(mappedElementIds)// ghost all, but show all visible
    // But show ALL (in case anything hidden before)
  } 
  else if (mode === 'mappedElements') {
    // Show mapped, hide non-mapped
    if (mappedElementIds.length)
      filtering.isolateObjects(mappedElementIds) // Show only these + ghost rest (by default)
    else
      filtering.resetFilters()
  }
  else if (mode === 'nonMappedElements') {
    // Show non-mapped, hide mapped
    if (nonMappedElementIds.length)
      filtering.hideObjects(mappedElementIds, undefined, false, true)
    else
      filtering.resetFilters()
  }
  else if (mode === 'noOverrides') {
    filtering.resetFilters()
    filtering.removeUserObjectColors()
    filtering.removeColorFilter()
    filtering.showObjects(allElementIds)
  }
}