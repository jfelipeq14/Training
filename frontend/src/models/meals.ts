// Meal category enum matching backend
export const CategoryEnum = {
  HAMBURGERS_AND_HOTDOGS: 'HAMBURGERS_AND_HOTDOGS',
  CHICKEN: 'CHICKEN',
  FISH: 'FISH',
  MEATS: 'MEATS',
  DESSERTS: 'DESSERTS',
  VEGAN_FOOD: 'VEGAN_FOOD',
  KIDS_MEALS: 'KIDS_MEALS',
} as const;

export type CategoryEnum = (typeof CategoryEnum)[keyof typeof CategoryEnum];

// Base meal interface
export interface MealBase {
  name: string;
  category: CategoryEnum;
  description: string;
  price_without_iva: number;
  is_available: boolean;
}

// Meal creation interface
export interface MealCreate extends MealBase {
  /** Name of the meal (will be converted to uppercase) */
  name: string;
  /** Category from enum */
  category: CategoryEnum;
  /** Description of the meal */
  description: string;
  /** Price without IVA (must be greater than 0) */
  price_without_iva: number;
  /** Availability status (default: true) */
  is_available: boolean;
}

// Meal update interface (all fields optional)
export interface MealUpdate {
  name?: string;
  category?: CategoryEnum;
  description?: string;
  price_without_iva?: number;
  is_available?: boolean;
}

// Meal response interface (from API)
export interface MealResponse extends MealBase {
  id: number;
  uuid: string;
  created_at: string; // ISO datetime string
  updated_at?: string; // ISO datetime string
}

// Meal list response interface
export interface MealListResponse {
  meals: MealResponse[];
  total: number;
}

// Validation functions (mirroring backend validation)
export const MealValidation = {
  validateName: (name: string): string => {
    if (!name || name.trim().length === 0) {
      throw new Error('El nombre del combo es requerido');
    }
    if (name.length > 255) {
      throw new Error('El nombre del combo no puede exceder 255 caracteres');
    }
    return name.toUpperCase();
  },

  validatePrice: (price: number): number => {
    if (price <= 0) {
      throw new Error('El precio debe ser mayor a 0');
    }
    // Round to 2 decimal places to match Decimal(10, 2)
    return Math.round(price * 100) / 100;
  },

  validateDescription: (description: string): string => {
    if (!description || description.trim().length === 0) {
      throw new Error('La descripción del combo es requerida');
    }
    return description.trim();
  },

  // Combined validation for meal creation
  validateMealCreate: (meal: MealCreate): MealCreate => {
    return {
      ...meal,
      name: MealValidation.validateName(meal.name),
      price_without_iva: MealValidation.validatePrice(meal.price_without_iva),
      description: MealValidation.validateDescription(meal.description),
    };
  },

  // Validation for meal update (only validate provided fields)
  validateMealUpdate: (meal: MealUpdate): MealUpdate => {
    const validated: MealUpdate = {};

    if (meal.name !== undefined) {
      validated.name = MealValidation.validateName(meal.name);
    }
    if (meal.price_without_iva !== undefined) {
      validated.price_without_iva = MealValidation.validatePrice(
        meal.price_without_iva
      );
    }
    if (meal.description !== undefined) {
      validated.description = MealValidation.validateDescription(
        meal.description
      );
    }
    if (meal.category !== undefined) {
      validated.category = meal.category;
    }
    if (meal.is_available !== undefined) {
      validated.is_available = meal.is_available;
    }

    return validated;
  },
};

// Type guards
export const isMealResponse = (obj: unknown): obj is MealResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'uuid' in obj &&
    'name' in obj &&
    'category' in obj &&
    'description' in obj &&
    'price_without_iva' in obj &&
    'is_available' in obj &&
    'created_at' in obj &&
    typeof (obj as MealResponse).id === 'number' &&
    typeof (obj as MealResponse).uuid === 'string' &&
    typeof (obj as MealResponse).name === 'string' &&
    typeof (obj as MealResponse).category === 'string' &&
    typeof (obj as MealResponse).description === 'string' &&
    typeof (obj as MealResponse).price_without_iva === 'number' &&
    typeof (obj as MealResponse).is_available === 'boolean' &&
    typeof (obj as MealResponse).created_at === 'string'
  );
};

export const isMealListResponse = (obj: unknown): obj is MealListResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'meals' in obj &&
    'total' in obj &&
    Array.isArray((obj as MealListResponse).meals) &&
    typeof (obj as MealListResponse).total === 'number' &&
    (obj as MealListResponse).meals.every(isMealResponse)
  );
};

// Category labels for display
export const CATEGORY_LABELS: Record<CategoryEnum, string> = {
  [CategoryEnum.HAMBURGERS_AND_HOTDOGS]: 'Hamburguesas y Perros',
  [CategoryEnum.CHICKEN]: 'Pollo',
  [CategoryEnum.FISH]: 'Pescado',
  [CategoryEnum.MEATS]: 'Carnes',
  [CategoryEnum.DESSERTS]: 'Postres',
  [CategoryEnum.VEGAN_FOOD]: 'Comida Vegana',
  [CategoryEnum.KIDS_MEALS]: 'Menú Infantil',
};

// Category options for forms
export const CATEGORY_OPTIONS = Object.entries(CATEGORY_LABELS).map(
  ([value, label]) => ({
    value: value as CategoryEnum,
    label,
  })
);

// Default empty meal for forms
export const EMPTY_MEAL: MealCreate = {
  name: '',
  category: CategoryEnum.HAMBURGERS_AND_HOTDOGS,
  description: '',
  price_without_iva: 0,
  is_available: true,
};

// Form field configurations
export const MEAL_FORM_FIELDS = {
  name: {
    label: 'Nombre del Combo',
    placeholder: 'SUPER CHEESE BURGER DOBLE',
    required: true,
    maxLength: 255,
    helpText: 'Nombre único del combo (máximo 255 caracteres)',
  },
  category: {
    label: 'Categoría',
    placeholder: 'Seleccionar categoría',
    required: true,
    helpText: 'Categoría del combo',
  },
  description: {
    label: 'Descripción',
    placeholder:
      'Hamburguesa pan de ajonjolí, doble carne de 200gr, queso cheddar...',
    required: true,
    helpText: 'Descripción detallada del combo',
  },
  price_without_iva: {
    label: 'Precio sin IVA',
    placeholder: '15000',
    required: true,
    type: 'number',
    min: 0.01,
    step: 0.01,
    helpText: 'Precio del combo sin incluir IVA (mayor a 0)',
  },
  is_available: {
    label: 'Disponibilidad',
    helpText: 'Marque si el combo está actualmente disponible',
  },
} as const;

// Price calculation utilities
export const MealCalculations = {
  // Calculate IVA (19% for Colombia)
  calculateIVA: (priceWithoutIVA: number): number => {
    return Math.round(priceWithoutIVA * 0.19 * 100) / 100;
  },

  // Calculate total price with IVA
  calculateTotalWithIVA: (priceWithoutIVA: number): number => {
    const iva = MealCalculations.calculateIVA(priceWithoutIVA);
    return Math.round((priceWithoutIVA + iva) * 100) / 100;
  },

  // Format price for display
  formatPrice: (price: number): string => {
    return new Intl.NumberFormat('es-CO', {
      style: 'currency',
      currency: 'COP',
      minimumFractionDigits: 2,
    }).format(price);
  },
};
