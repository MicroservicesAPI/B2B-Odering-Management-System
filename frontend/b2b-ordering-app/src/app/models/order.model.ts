// src/app/models/order.model.ts

export interface OrderItemCreate {
  product_name: string;
  quantity: number;
}

export interface OrderCreateRequest {
  description?: string;
  items: OrderItemCreate[];
}

export interface OrderItem {
  product_name: string;
  quantity: number;
}

export interface Order {
  id: string;
  user_id: string;
  department_id: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'DELIVERED';
  description?: string;
  created_at: string;
  items: OrderItem[];
}
