// Base order interface
export interface OrderBase {
  document: string;
  meal_uuid: string;
  quantity: number;
  additional_info: string;
}

// Order creation interface
export interface OrderCreate extends OrderBase {
  /** Customer document number */
  document: string;
  /** UUID of the meal/combo */
  meal_uuid: string;
  /** Quantity (1-99) */
  quantity: number;
  /** Additional information (max 511 chars) */
  additional_info: string;
}

// Order update interface (only for delivery timestamp)
export interface OrderUpdate {
  /** Delivery timestamp */
  timestamp: string; // ISO datetime string
}

// Order response interface (from API)
export interface OrderResponse extends OrderBase {
  id: number;
  uuid: string;
  order_date: string; // ISO datetime string
  document: string;
  meal_uuid: string;
  quantity: number;
  additional_info: string;
  subtotal_without_iva: number;
  iva_amount: number;
  total_with_iva: number;
  is_delivered: boolean;
  delivery_date?: string; // ISO datetime string
  created_at: string; // ISO datetime string
  updated_at?: string; // ISO datetime string
}

// Order response with additional details (customer and meal info)
export interface OrderResponseWithDetails extends OrderResponse {
  customer_name?: string;
  meal_name?: string;
  meal_category?: string;
}

// Order list response interface
export interface OrderListResponse {
  orders: OrderResponse[];
  total: number;
}

// Order status enum for easier handling
export const OrderStatus = {
  PENDING: 'PENDING',
  DELIVERED: 'DELIVERED',
} as const;

export type OrderStatus = (typeof OrderStatus)[keyof typeof OrderStatus];

// Validation functions (mirroring backend validation)
export const OrderValidation = {
  validateQuantity: (quantity: number): number => {
    if (!Number.isInteger(quantity)) {
      throw new Error('La cantidad debe ser un número entero');
    }
    if (quantity < 1 || quantity >= 100) {
      throw new Error('La cantidad debe ser entre 1 y 99');
    }
    return quantity;
  },

  validateDocument: (document: string): string => {
    if (!document || document.trim().length === 0) {
      throw new Error('El documento del cliente es requerido');
    }
    return document.trim();
  },

  validateMealUuid: (uuid: string): string => {
    if (!uuid || uuid.trim().length === 0) {
      throw new Error('El UUID del combo es requerido');
    }
    // Basic UUID validation (format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    const uuidRegex =
      /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
    if (!uuidRegex.test(uuid)) {
      throw new Error('El UUID del combo no tiene un formato válido');
    }
    return uuid;
  },

  validateAdditionalInfo: (info: string): string => {
    if (info && info.length > 511) {
      throw new Error(
        'La información adicional no puede exceder 511 caracteres'
      );
    }
    return info || '';
  },

  validateTimestamp: (timestamp: string): string => {
    if (!timestamp) {
      throw new Error('La fecha de entrega es requerida');
    }
    const date = new Date(timestamp);
    if (isNaN(date.getTime())) {
      throw new Error('La fecha de entrega no es válida');
    }
    // Ensure it's not in the past
    const now = new Date();
    if (date < now) {
      throw new Error('La fecha de entrega no puede ser en el pasado');
    }
    return timestamp;
  },

  // Combined validation for order creation
  validateOrderCreate: (order: OrderCreate): OrderCreate => {
    return {
      ...order,
      document: OrderValidation.validateDocument(order.document),
      meal_uuid: OrderValidation.validateMealUuid(order.meal_uuid),
      quantity: OrderValidation.validateQuantity(order.quantity),
      additional_info: OrderValidation.validateAdditionalInfo(
        order.additional_info
      ),
    };
  },

  // Validation for order update
  validateOrderUpdate: (order: OrderUpdate): OrderUpdate => {
    return {
      timestamp: OrderValidation.validateTimestamp(order.timestamp),
    };
  },
};

// Type guards
export const isOrderResponse = (obj: unknown): obj is OrderResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'uuid' in obj &&
    'order_date' in obj &&
    'document' in obj &&
    'meal_uuid' in obj &&
    'quantity' in obj &&
    'additional_info' in obj &&
    'subtotal_without_iva' in obj &&
    'iva_amount' in obj &&
    'total_with_iva' in obj &&
    'is_delivered' in obj &&
    'created_at' in obj &&
    typeof (obj as OrderResponse).id === 'number' &&
    typeof (obj as OrderResponse).uuid === 'string' &&
    typeof (obj as OrderResponse).order_date === 'string' &&
    typeof (obj as OrderResponse).document === 'string' &&
    typeof (obj as OrderResponse).meal_uuid === 'string' &&
    typeof (obj as OrderResponse).quantity === 'number' &&
    typeof (obj as OrderResponse).additional_info === 'string' &&
    typeof (obj as OrderResponse).subtotal_without_iva === 'number' &&
    typeof (obj as OrderResponse).iva_amount === 'number' &&
    typeof (obj as OrderResponse).total_with_iva === 'number' &&
    typeof (obj as OrderResponse).is_delivered === 'boolean' &&
    typeof (obj as OrderResponse).created_at === 'string'
  );
};

export const isOrderResponseWithDetails = (
  obj: unknown
): obj is OrderResponseWithDetails => {
  return (
    (isOrderResponse(obj) &&
      (obj as OrderResponseWithDetails).customer_name === undefined) ||
    typeof (obj as OrderResponseWithDetails).customer_name === 'string'
  );
};

export const isOrderListResponse = (obj: unknown): obj is OrderListResponse => {
  return (
    obj !== null &&
    typeof obj === 'object' &&
    obj !== null &&
    'orders' in obj &&
    'total' in obj &&
    Array.isArray((obj as OrderListResponse).orders) &&
    typeof (obj as OrderListResponse).total === 'number' &&
    (obj as OrderListResponse).orders.every(isOrderResponse)
  );
};

// Order status utilities
export const OrderUtils = {
  getStatus: (order: OrderResponse): OrderStatus => {
    return order.is_delivered ? OrderStatus.DELIVERED : OrderStatus.PENDING;
  },

  getStatusLabel: (status: OrderStatus): string => {
    return status === OrderStatus.DELIVERED ? 'Entregado' : 'Pendiente';
  },

  getStatusBadgeClass: (status: OrderStatus): string => {
    return status === OrderStatus.DELIVERED ? 'delivered' : 'pending';
  },

  // Format dates for display
  formatDate: (dateString: string): string => {
    return new Date(dateString).toLocaleString('es-CO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  },

  // Format short date (without time)
  formatShortDate: (dateString: string): string => {
    return new Date(dateString).toLocaleDateString('es-CO', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
    });
  },

  // Truncate UUID for display
  truncateUuid: (uuid: string, length: number = 8): string => {
    return uuid.substring(0, length) + '...';
  },
};

// Price calculation utilities (same as meals but for orders)
export const OrderCalculations = {
  // Calculate IVA (19% for Colombia)
  calculateIVA: (priceWithoutIVA: number): number => {
    return Math.round(priceWithoutIVA * 0.19 * 100) / 100;
  },

  // Calculate total price with IVA
  calculateTotalWithIVA: (priceWithoutIVA: number): number => {
    const iva = OrderCalculations.calculateIVA(priceWithoutIVA);
    return Math.round((priceWithoutIVA + iva) * 100) / 100;
  },

  // Calculate order totals based on meal price and quantity
  calculateOrderTotals: (priceWithoutIVA: number, quantity: number) => {
    const subtotal = Math.round(priceWithoutIVA * quantity * 100) / 100;
    const ivaAmount = OrderCalculations.calculateIVA(subtotal);
    const total = Math.round((subtotal + ivaAmount) * 100) / 100;

    return {
      subtotal_without_iva: subtotal,
      iva_amount: ivaAmount,
      total_with_iva: total,
    };
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

// Default empty order for forms
export const EMPTY_ORDER: OrderCreate = {
  document: '',
  meal_uuid: '',
  quantity: 1,
  additional_info: '',
};

// Form field configurations
export const ORDER_FORM_FIELDS = {
  document: {
    label: 'Documento del Cliente',
    placeholder: 'CC-12345678',
    required: true,
    helpText: 'Documento del cliente que realiza el pedido',
  },
  meal_uuid: {
    label: 'Combo',
    placeholder: 'Seleccionar combo',
    required: true,
    helpText: 'UUID del combo a ordenar',
  },
  quantity: {
    label: 'Cantidad',
    placeholder: '1',
    required: true,
    type: 'number',
    min: 1,
    max: 99,
    helpText: 'Cantidad de combos (1-99)',
  },
  additional_info: {
    label: 'Información Adicional',
    placeholder: 'Sin salsa de tomate, extra queso...',
    maxLength: 511,
    helpText: 'Instrucciones especiales para el pedido (opcional)',
  },
} as const;

// Order status options for filters
export const ORDER_STATUS_OPTIONS = [
  { value: '', label: 'Todos los estados' },
  { value: 'false', label: 'Pendientes' },
  { value: 'true', label: 'Entregados' },
];

// Order statistics interface
export interface OrderStats {
  total: number;
  pending: number;
  delivered: number;
  totalRevenue: number;
  pendingRevenue: number;
  deliveredRevenue: number;
}

// Calculate statistics from orders
export const calculateOrderStats = (orders: OrderResponse[]): OrderStats => {
  const total = orders.length;
  const pending = orders.filter(order => !order.is_delivered).length;
  const delivered = orders.filter(order => order.is_delivered).length;

  const totalRevenue = orders.reduce(
    (sum, order) => sum + order.total_with_iva,
    0
  );
  const pendingRevenue = orders
    .filter(order => !order.is_delivered)
    .reduce((sum, order) => sum + order.total_with_iva, 0);
  const deliveredRevenue = orders
    .filter(order => order.is_delivered)
    .reduce((sum, order) => sum + order.total_with_iva, 0);

  return {
    total,
    pending,
    delivered,
    totalRevenue,
    pendingRevenue,
    deliveredRevenue,
  };
};
