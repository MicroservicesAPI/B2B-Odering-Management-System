export interface User {
  id: string;
  email: string;
  role: 'admin' | 'staff';
  department_id?: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user: User;
}

export interface RegisterRequest {
  email: string;
  password: string;
  role: 'ADMIN' | 'STAFF';
  department_id?: string;
}
