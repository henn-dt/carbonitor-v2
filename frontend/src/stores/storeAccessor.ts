// src/stores/storeAccessor.ts
import { useAuthStore } from '@/stores/authStore';
import { useCategoryStore } from '@/stores/categoryStore';
import { useUsersStore } from '@/stores/usersStore';
import { useProductStore } from '@/stores/productStore';
import { useBuildupStore } from '@/stores/buildupStore';
import { useProductSnapshotStore } from '@/stores//productSnapshotStore';
import { useUiModalStore } from './uiModalStore';

// Store singletons with proper typing
let _authStore: ReturnType<typeof useAuthStore> | null = null;
let _categoryStore: ReturnType<typeof useCategoryStore> | null = null;
let _usersStore: ReturnType<typeof useUsersStore> | null = null;
let _productStore: ReturnType<typeof useProductStore> | null = null;
let _productSnapshotStore : ReturnType<typeof useProductSnapshotStore> | null = null;
let _buildupStore: ReturnType<typeof useBuildupStore> | null = null;
let _uiModalStore: ReturnType<typeof useUiModalStore> | null = null;

export function initializeStores() {
  _authStore = useAuthStore();
  _categoryStore = useCategoryStore();
  _usersStore = useUsersStore();
  _productStore = useProductStore();
  _buildupStore = useBuildupStore();
  _productSnapshotStore = useProductSnapshotStore();
  _uiModalStore = useUiModalStore()
}

// Getters for each store with guaranteed non-null return
export function getAuthStore(): ReturnType<typeof useAuthStore> {
  if (!_authStore) {
    _authStore = useAuthStore();
  } else {
    console.log("[StoreAccessor] Using existing auth store");
  }
  return _authStore;
}

export function getUiModalStore(): ReturnType<typeof useUiModalStore> {
  if (!_uiModalStore) {
    _uiModalStore = useUiModalStore();
  } else {
    console.log("[StoreAccessor] Using existing uiModal store");
  }
  return _uiModalStore;
}

export function getCategoryStore(): ReturnType<typeof useCategoryStore> {
  if (!_categoryStore) {
    console.log("[StoreAccessor] Category store created");
    _categoryStore = useCategoryStore();
  }
  return _categoryStore;
}

export function getUsersStore(): ReturnType<typeof useUsersStore> {
  if (!_usersStore) {
    console.log("[StoreAccessor] Users store created");
    _usersStore = useUsersStore();
  }
  return _usersStore;
}

export function getProductStore(): ReturnType<typeof useProductStore> {
  if (!_productStore) {
    console.log("[StoreAccessor] Product store created");
    _productStore = useProductStore();
  }
  return _productStore;
}

export function getProductSnapshotStore(): ReturnType<typeof useProductSnapshotStore> {
  if (!_productSnapshotStore) {
    console.log("[StoreAccessor] Product snapshot store created");
    _productSnapshotStore = useProductSnapshotStore();
  }
  return _productSnapshotStore;
}

export function getBuildupStore(): ReturnType<typeof useBuildupStore> {
  if (!_buildupStore) {
    console.log("[StoreAccessor] Buildup store created");
    _buildupStore = useBuildupStore();
  }
  return _buildupStore;
}

// Method to check if stores are already initialized
export function areStoresInitialized(): boolean {
  return _authStore !== null && 
          _uiModalStore !== null &&
         _categoryStore !== null && 
         _usersStore !== null && 
         _buildupStore !== null &&
         _productStore !== null &&
         _productSnapshotStore !== null
}