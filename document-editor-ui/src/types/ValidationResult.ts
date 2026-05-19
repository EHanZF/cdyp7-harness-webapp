// src/types/ValidationResult.ts

/**
 * Validation result returned from backend
 */
export interface ValidationResult {
    valid: boolean;
    errors?: string[];
    warnings?: string[];
}
