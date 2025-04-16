<template>
<div class="page-content">
    <!-- Header and Title -->
    <h1 class="title">Categories</h1>
    <h2 class="subtitle">this page lists all categories from the database</h2>

    <div v-if="loading" class="loading-indicator">
      Loading categories...
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    <template v-if="!loading && !error">
    <!-- Group categories by type -->
    <div v-for="type in allCategoryTypes" :key="type" class="section-container" :id="`${type.toLowerCase()}Section`">
      <div class="section-header" @click="toggleSection(`${type.toLowerCase()}Section`)">
        <a>{{ type }}</a>
        <span class="chevron">▼</span>
      </div>
      <div class="section-content">
        <!-- Add Category Card -->
        <div class="card add" @click="openCreateModal(type)">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"></line>
            <line x1="5" y1="12" x2="19" y2="12"></line>
          </svg>
          <p>Add Category</p>
        </div>
        
        <!-- Category Cards -->
        <div v-for="category in getCategoriesByType(type)" :key="category.id" class="card" @click="openEditModal(category)">
          <div class="card-name"  >{{ category.name }} </div>
          <div class="card-description">{{ category.description }}</div>
          <div class="card-list" v-if="category.property_schema">
            <div class="list-title">Properties:</div>
            <ul class="list-items">
              <li v-for="(property, propId) in category.property_schema" :key="propId">
                {{ property.name }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    </template>

    <!-- The modal component -->
    <CategoryModal 
      v-if="showModal" 
      :data="selectedCategory" 
      :isNew="isNewCategory"
      :isSaving="saving"
      :section-type="sectionType"
      :existing-categories="categories"
      @close="closeModal"
      @save="handleSaveCategory"
      @delete="handleDeleteCategory"
    />
    
    <div v-if="showDebugInfo" class="debug-info">
      <pre>{{ JSON.stringify(categories, null, 2) }}</pre>
    </div>
  </div>


</template>

<script lang="ts">
import { defineComponent, ref, onMounted, computed, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import type { ICategory } from '@/types/category/ICategory';
import CategoryModal from '@/views/user/components/categories/CategoryModal.vue';
import { CategoryEntityType } from '@/types/category/CategoryEntityTypeEnum';
import { getCategoryService } from '@/services/ServiceAccessor';
export default defineComponent({
  name: 'CategoriesView',
  components: {
    CategoryModal
  },
  setup() {
    const router = useRouter();

    const categoryService = getCategoryService();
    if (!categoryService) {
      throw new Error('CategoryService not provided');
    }

    // State management
    const categories = ref<ICategory[]>([]);
    const loading = ref(true);
    const saving = ref(false);
    const error = ref<string | undefined>(undefined);
    const showModal = ref(false);
    const dataLoaded = ref(false);
    const showDebugInfo = ref(false);
    const selectedCategory = ref<ICategory | null>(null);
    const isNewCategory = ref(true);
    const sectionType = ref<CategoryEntityType>(CategoryEntityType.Other);

    // Get all possible category types from the enum
    const allCategoryTypes = Object.values(CategoryEntityType);

    // Subscribe to category changes
    let unsubscribe: (() => void) | null = null;
      
    
    // Function to get categories by type
    const getCategoriesByType = (type: string) => {
      return categories.value.filter(category =>         
        CategoryEntityType[category.type] === type
      );
    };




    // Modal control functions
    const openCreateModal = (type: string) => {
      isNewCategory.value = true;
      selectedCategory.value = null;
      sectionType.value = CategoryEntityType[type as keyof typeof CategoryEntityType]
      showModal.value = true;

    };
    
    const openEditModal = async (category: ICategory) => {
      try {
        isNewCategory.value = false;
        // Fetch the latest data for this category before editing
        const freshCategory = await categoryService.getCategoryById(category.id);
        selectedCategory.value = freshCategory;
        showModal.value = true;
      } catch (err) {
        console.error('Error fetching category details:', err);
      }
    };
    
    const closeModal = () => {
      
      showModal.value = false;
      // Clear selected category after animation completes
      setTimeout(() => {
        selectedCategory.value = null;
      }, 300);
    };
    

    // Service interaction methods

    const loadCategories = async () => {           
            try {
            loading.value = true;

            // Get categories from the service
            const data = await categoryService.getCategories();
            categories.value = data;

            // Get entities if needed
            // categoryEntities.value = await categoryService.getCategoryEntities();

            dataLoaded.value = true;

            // Subscribe to future changes
            if (!unsubscribe) {
              unsubscribe = categoryService.subscribeToCategories((updatedCategories) => {
              categories.value = updatedCategories;
            });
            }
          } catch (err) {
            error.value = err instanceof Error ? err.message : 'Failed to load categories';
            console.error('Error loading categories:', err);
          } finally {
            loading.value = false;
          }
        }

    const clearError = async () => {
        try {
            error.value = ""
        }
        catch (err) {
            console.error('Error clearing errors:', err);
        }
    }

    const handleSaveCategory = async (categoryData: ICategory) => {
      try {
        if (isNewCategory.value) {
          // Create new category
          await categoryService.createCategory(categoryData);
        } else {
          // Update existing category
          await categoryService.updateCategory(categoryData.id, categoryData);
        }

        
        closeModal();
      } catch (err) {
        console.error('Error saving category:', err);
      }
    };
    
    const handleDeleteCategory = async (categoryId: number) => {
      try {
        await categoryService.deleteCategory(categoryId);

        closeModal();
      } catch (err) {
        console.error('Error deleting category:', err);
      }
    };

    // Helper methods
    
    const toggleSection = (sectionId: string) => {
      const section = document.getElementById(sectionId);
      if (section) {
        section.classList.toggle('collapsed');
      }
    };
        

    
    // Initial Load
    onMounted(async () => {

        clearError()
        loadCategories()
        });

    onUnmounted(() => {
      // Clean up subscription
      if (unsubscribe) {
        unsubscribe();
      }
    });

    return {
    //State
      categories,
      allCategoryTypes,
      loading,
      error,
      showDebugInfo,
      selectedCategory,
      isNewCategory,
      saving,
      showModal,
      sectionType,

      //Methods
      toggleSection,
      loadCategories,
      getCategoriesByType,
      openCreateModal,
      openEditModal,
      closeModal,
      handleSaveCategory,
      handleDeleteCategory,
      clearError
    };
  }
});
</script>

<style scoped>
.loading-indicator {
  text-align: center;
  padding: 20px;
}

.error-message {
  color: red;
  padding: 15px;
  background-color: #ffeeee;
  border-radius: 5px;
  margin: 15px 0;
}

.debug-info {
  margin-top: 30px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 5px;
  overflow: auto;
}
</style>