export interface Product {
  id: string;
  name: string;
  sku: string;
  description: string;
  stock_quantity: number;
  min_stock: number;
  created_at: string;
}

export interface ProductCreateRequest {
  name: string;
  sku: string;
  description: string;
  stock_quantity: number;
  min_stock: number;
}
