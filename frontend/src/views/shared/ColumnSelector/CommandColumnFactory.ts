// commandColumnFactory.ts
import { ColumnType } from '@/views/shared/ColumnSelector/ColumnType';
import type { ColumnDefinition } from '@/views/shared/ColumnSelector/ColumnDefinition';
import type { Component } from 'vue';

export interface CommandColumnOptions {
    key?: string;
    label?: string;
    minWidth?: number;
    maxWidth?: number;
    tooltip?: string;
    visible?: boolean;
    commandComponent?: Component;
    position?: 'start' | 'end'; // Where to place the command column
  }

export function createCommandColumn(options: CommandColumnOptions = {}): ColumnDefinition {
    return {
        key: options.key || 'actions',
        label: options.label || 'Actions',
        default: true,
        visible: options.visible !== undefined ? options.visible : true,
        tooltip: options.tooltip || 'Available actions',
        columnProperties: {
          type: ColumnType.command,
          minWidth: options.minWidth || 120,
          maxWidth: options.maxWidth || 200,
          defaultValue: null
        },
        columnValues: [],
        // Store the command component in metadata
        metadata: options.commandComponent ? {
          commandComponent: options.commandComponent
        } : undefined
      };
  }