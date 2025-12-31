export interface Order {
  id: string;
  department_id: string;
  user_id: string;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'DELIVERED';
  total_amount: number;
  created_at: string;
  updated_at: string;
  items?: OrderItem[];
}

export interface OrderItem {
  id: string;
  order_id: string;
  product_id: string;
  quantity: number;
  unit_price: number;
  total_price: number;
}

export interface OrderCreateRequest {
  department_id: string;
  items: {
    product_id: string;
    quantity: number;
  }[];
}
