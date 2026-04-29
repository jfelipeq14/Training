// Base customer interface
export interface CustomerBase {
  document_number: string;
  full_name: string;
  email: string;
  phone_number: string;
  address: string;
}

// Customer creation interface (with validation rules)
export interface CustomerCreate extends CustomerBase {
  /** Must match format TIPO-NUMERO (CC-12345678, CE-123456, P-1234567) */
  document_number: string;
  /** Full name of the customer */
  full_name: string;
  /** Valid email address */
  email: string;
  /** Phone number with 7-10 digits */
  phone_number: string;
  /** Complete delivery address */
  address: string;
}

// Customer update interface (all fields optional)
export interface CustomerUpdate {
  full_name?: string;
  email?: string;
  phone_number?: string;
  address?: string;
}

// Customer response interface (from API)
export interface CustomerResponse extends CustomerBase {
  id: number;
  created_at: string; // ISO datetime string
  updated_at?: string; // ISO datetime string
}

// Customer list response interface
export interface CustomerListResponse {
  customers: CustomerResponse[];
  total: number;
}

// Validation functions (mirroring backend validation)
export const CustomerValidation = {
  validateDocumentFormat: (document: string): string => {
    const regex = /^[A-Z]{1,3}-\d+$/;
    if (!regex.test(document.toUpperCase())) {
      throw new Error(
        'El documento debe tener formato TIPO-NUMERO (ej: CC-12345678)'
      );
    }
    return document.toUpperCase();
  },

  validatePhoneNumber: (phone: string): string => {
    if (!/^\d+$/.test(phone)) {
      throw new Error('El número de celular debe contener solo dígitos');
    }
    if (phone.length < 7 || phone.length > 10) {
      throw new Error('El número de celular debe tener entre 7 y 10 dígitos');
    }
    return phone;
  },

  validateEmail: (email: string): string => {
    if (!email.includes('@') || !email.split('@')[1]?.includes('.')) {
      throw new Error('Email inválido');
    }
    return email.toLowerCase();
  },

  // Combined validation for customer creation
  validateCustomerCreate: (customer: CustomerCreate): CustomerCreate => {
    return {
      ...customer,
      document_number: CustomerValidation.validateDocumentFormat(
        customer.document_number
      ),
      phone_number: CustomerValidation.validatePhoneNumber(
        customer.phone_number
      ),
      email: CustomerValidation.validateEmail(customer.email),
    };
  },

  // Validation for customer update (only validate provided fields)
  validateCustomerUpdate: (customer: CustomerUpdate): CustomerUpdate => {
    const validated: CustomerUpdate = {};

    if (customer.full_name !== undefined) {
      validated.full_name = customer.full_name;
    }
    if (customer.email !== undefined) {
      validated.email = CustomerValidation.validateEmail(customer.email);
    }
    if (customer.phone_number !== undefined) {
      validated.phone_number = CustomerValidation.validatePhoneNumber(
        customer.phone_number
      );
    }
    if (customer.address !== undefined) {
      validated.address = customer.address;
    }

    return validated;
  },
};

// Type guards
export const isCustomerResponse = (obj: unknown): obj is CustomerResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'document_number' in obj &&
    'full_name' in obj &&
    'email' in obj &&
    'phone_number' in obj &&
    'address' in obj &&
    'created_at' in obj &&
    typeof (obj as CustomerResponse).id === 'number' &&
    typeof (obj as CustomerResponse).document_number === 'string' &&
    typeof (obj as CustomerResponse).full_name === 'string' &&
    typeof (obj as CustomerResponse).email === 'string' &&
    typeof (obj as CustomerResponse).phone_number === 'string' &&
    typeof (obj as CustomerResponse).address === 'string' &&
    typeof (obj as CustomerResponse).created_at === 'string'
  );
};

export const isCustomerListResponse = (
  obj: unknown
): obj is CustomerListResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'customers' in obj &&
    'total' in obj &&
    Array.isArray((obj as CustomerListResponse).customers) &&
    typeof (obj as CustomerListResponse).total === 'number' &&
    (obj as CustomerListResponse).customers.every(isCustomerResponse)
  );
};

// Default empty customer for forms
export const EMPTY_CUSTOMER: CustomerCreate = {
  document_number: '',
  full_name: '',
  email: '',
  phone_number: '',
  address: '',
};

// Document type options for forms
export const DOCUMENT_TYPES = [
  { value: 'CC', label: 'Cédula de Ciudadanía' },
  { value: 'CE', label: 'Cédula de Extranjería' },
  { value: 'P', label: 'Pasaporte' },
  { value: 'TI', label: 'Tarjeta de Identidad' },
];

// Form field configurations
export const CUSTOMER_FORM_FIELDS = {
  document_number: {
    label: 'Número de Documento',
    placeholder: 'CC-12345678',
    required: true,
    maxLength: 20,
    pattern: '[A-Z]{1,3}-[0-9]+',
    helpText: 'Formato: TIPO-NUMERO (ej: CC-12345678)',
  },
  full_name: {
    label: 'Nombre Completo',
    placeholder: 'Juan Pérez García',
    required: true,
    maxLength: 255,
    helpText: 'Nombre y apellido completo',
  },
  email: {
    label: 'Email',
    placeholder: 'juan.perez@example.com',
    required: true,
    maxLength: 255,
    type: 'email',
    helpText: 'Email válido para notificaciones',
  },
  phone_number: {
    label: 'Número de Celular',
    placeholder: '3001234567',
    required: true,
    maxLength: 10,
    minLength: 7,
    pattern: '[0-9]+',
    type: 'tel',
    helpText: '7-10 dígitos sin espacios ni guiones',
  },
  address: {
    label: 'Dirección de Envío',
    placeholder: 'Calle 123 #45-67, Bogotá',
    required: true,
    maxLength: 500,
    helpText: 'Dirección completa para entregas',
  },
} as const;
