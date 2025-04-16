// stores/uiModalStore.ts
import { defineStore } from 'pinia';
import { type ModalEntry } from '@/types/modal/IModal';


export const useUiModalStore = defineStore('uiModal', {
    state: () => ({
      modals: [] as ModalEntry[]   // stack of open modals
    }),
    getters: {
      activeModal: (state) => state.modals.length > 0 ? state.modals[state.modals.length - 1] : null
    },
    actions: {
      openModal(modal: ModalEntry) {
        this.modals.push(modal);
      },
      closeModal() {
        this.modals.pop();
      },
      closeAllModals() {
        this.modals = [];
      }
    }
  });