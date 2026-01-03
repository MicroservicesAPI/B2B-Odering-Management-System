// src/app/pages/make-order/make-order.component.ts

import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ProductService } from '../../services/product.service';
import { OrderService } from '../../services/order.service';
import { Product } from '../../models/product.model';
import { OrderCreateRequest, OrderItemCreate } from '../../models/order.model';

@Component({
  selector: 'app-make-order',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './make-order.component.html',
  styleUrls: ['./make-order.component.scss']
})
export class MakeOrderComponent implements OnInit {
  products: Product[] = [];
  quantities: Record<string, number> = {};
  description = '';
  loading = false;
  errorMessage = '';

  constructor(
    private productService: ProductService,
    private orderService: OrderService
  ) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.productService.getProducts().subscribe({
      next: products => this.products = products,
      error: () => this.errorMessage = 'Failed to load products'
    });
  }

  placeOrder(): void {
    const items: OrderItemCreate[] = this.products
      .filter(p => this.quantities[p.name] && this.quantities[p.name] > 0)
      .map(p => ({
        product_name: p.name,
        quantity: this.quantities[p.name]
      }));

    if (items.length === 0) {
      this.errorMessage = 'Please select at least one product';
      return;
    }

    const order: OrderCreateRequest = {
      description: this.description,
      items
    };

    this.loading = true;
    this.errorMessage = '';

    this.orderService.createOrder(order).subscribe({
      next: () => {
        this.loading = false;
        alert('Order placed successfully');
        this.quantities = {};
        this.description = '';
      },
      error: err => {
        this.loading = false;
        this.errorMessage = err.error?.detail || 'Order failed';
      }
    });
  }
}
