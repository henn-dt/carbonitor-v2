// frontend/src/views/user/components/categories/CategoryPropertyValidation.ts
import { CategoryPropertyFormat } from '@/types/category/CategoryPropertyFormatEnum';

export function validateCategoryPropertyValue(
  value: any, 
  format: CategoryPropertyFormat, 
  allowEmpty: boolean = true,
  validateUnique: boolean = false,
  existingValues: Array<string | number | boolean | null> = []
): { isValid: boolean; error: string } {
  let error = '';
  
  // Handle empty values
  if (value === null || value === undefined || value === '') {
    if (!allowEmpty) {
      return { isValid: false, error: 'Value cannot be empty' };
    }
    return { isValid: true, error: '' };
  }

  // Format-specific validation
  switch (format) {
    case CategoryPropertyFormat.NUMBER:
      if (typeof value === 'string') {
        const num = Number(value);
        if (isNaN(num)) {
          return { isValid: false, error: 'Value must be a valid number' };
        }
      } else if (typeof value !== 'number') {
        return { isValid: false, error: 'Value must be a number' };
      }
      break;
    case CategoryPropertyFormat.BOOLEAN:
      if (value !== true && value !== false) {
        return { isValid: false, error: 'Value must be true or false' };
      }
      break;
    case CategoryPropertyFormat.DATE:
      // Basic date validation
      const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
      if (typeof value !== 'string' || !dateRegex.test(value)) {
        return { isValid: false, error: 'Value must be a valid date (YYYY-MM-DD)' };
      }
      break;
  }

  // Validate uniqueness if required
  if (validateUnique && existingValues.some(v => v === value)) {
    return { isValid: false, error: 'This value already exists' };
  }

  return { isValid: true, error: '' };
}