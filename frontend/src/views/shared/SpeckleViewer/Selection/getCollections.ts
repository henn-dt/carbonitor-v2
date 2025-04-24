// frontend/src/views/shared/SpeckleViewer/Selection/getCollections.ts

import {
    Viewer, type TreeNode
  } from '@speckle/viewer';

export function getAllCollectionNodesIds(viewer : Viewer) {
  // We'll return node ids to select
  const nodes = viewer.getWorldTree().findAll((node) => {
    // Defensive: some top nodes may not have .model or .raw
    if (!node.model || !node.model.raw) return false;
    const raw = node.model.raw;
    // Must be a Speckle.Collection
    return (
      raw.speckle_type &&
      raw.speckle_type === "Speckle.Core.Models.Collection" 
    );
  });
  // Return their Speckle ids as strings
  return nodes.map(n => n.model.id);
}


export function getCollectionNodeIdsByNames(viewer : Viewer, collectionNames : String[]) {
    // We'll return node ids to select
    const nodes = viewer.getWorldTree().findAll((node) => {
      // Defensive: some top nodes may not have .model or .raw
      if (!node.model || !node.model.raw) return false;
      const raw = node.model.raw;
      // Must be a Speckle.Collection and have a name in our list
      return (
        raw.speckle_type &&
        raw.speckle_type === "Speckle.Core.Models.Collection" &&
        collectionNames.includes(raw.name)
      );
    });
    // Return their Speckle ids as strings
    return nodes.map(n => n.model.id);
  }

  export function getCollectionNodeIdsByExcludedNames(viewer : Viewer, collectionNames : String[]) {
    // We'll return node ids to select
    const nodes = viewer.getWorldTree().findAll((node) => {
      // Defensive: some top nodes may not have .model or .raw
      if (!node.model || !node.model.raw) return false;
      const raw = node.model.raw;
      // Must be a Speckle.Collection and have a name in our list
      return (
        raw.speckle_type &&
        raw.speckle_type === "Speckle.Core.Models.Collection" &&
        !collectionNames.includes(raw.name)
      );
    });
    // Return their Speckle ids as strings
    return nodes.map(n => n.model.id);
  }


  export function getElementIdsUnderCollectionNodes(viewer: Viewer, nodeIds: string[]): string[] {
    const worldTree = viewer.getWorldTree()
    let ids: string[] = []
    for (const id of nodeIds) {
      const nodes = worldTree.findId(id)
      if (!nodes) return []
      for (const node of nodes) {
        collectElementIdsForNode(node, ids)
      }
    }
    return ids
  }

  function collectElementIdsForNode(node: TreeNode, collector: string[]) {
    // If this node is a collection, recurse into its children
    if (node.model.raw?.speckle_type === "Speckle.Core.Models.Collection") {
      for (const child of node.children) {
        collectElementIdsForNode(child, collector)
      }
    } else {
      // Not a collection = an actual element, add id
      collector.push(node.model.id)
    }
  }
