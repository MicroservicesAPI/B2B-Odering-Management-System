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
  sortedProducts: Product[] = [];
  sortKey: 'name' | 'sku' = 'name';
  sortAsc = true;

  selectedProduct?: Product;
  quantity = 1;
  description = '';
  showModal = false;
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
      next: products => {
        this.products = products;
        this.sortProducts();
      },
      error: () => this.errorMessage = 'Failed to load products'
    });
  }

  sortProducts(): void {
    this.sortedProducts = [...this.products].sort((a, b) => {
      const valA = a[this.sortKey].toLowerCase();
      const valB = b[this.sortKey].toLowerCase();
      if (valA < valB) return this.sortAsc ? -1 : 1;
      if (valA > valB) return this.sortAsc ? 1 : -1;
      return 0;
    });
  }

  toggleSort(key: 'name' | 'sku'): void {
    if (this.sortKey === key) this.sortAsc = !this.sortAsc;
    else {
      this.sortKey = key;
      this.sortAsc = true;
    }
    this.sortProducts();
  }

  openModal(product: Product): void {
    this.selectedProduct = product;
    this.quantity = 1;
    this.description = '';
    this.showModal = true;
    this.errorMessage = '';
  }

  placeOrder(): void {
    if (!this.selectedProduct || this.quantity <= 0) {
      this.errorMessage = 'Please enter a valid quantity';
      return;
    }

    const order: OrderCreateRequest = {
      description: this.description,
      items: [{ product_name: this.selectedProduct.name, quantity: this.quantity }]
    };

    this.loading = true;
    this.orderService.createOrder(order).subscribe({
      next: () => {
        this.loading = false;
        alert(`Order placed for ${this.selectedProduct!.name}`);
        this.showModal = false;
      },
      error: err => {
        this.loading = false;
        this.errorMessage = err.error?.detail || 'Order failed';
      }
    });
  }

  closeModal(): void {
    this.showModal = false;
  }
}
