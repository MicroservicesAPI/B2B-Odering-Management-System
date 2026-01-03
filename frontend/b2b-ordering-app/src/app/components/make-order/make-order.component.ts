import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';
import { OrderService } from '../../services/order.service';
import { Product } from '../../models/product.model';
import { OrderCreateRequest } from '../../models/order.model';
import { FormsModule } from '@angular/forms';
import {NgForOf, NgIf} from '@angular/common';

@Component({
  selector: 'app-make-order',
  templateUrl: './make-order.component.html',
  styleUrls: ['./make-order.component.scss'],
  imports: [FormsModule, NgIf, NgForOf]
})
export class MakeOrderComponent implements OnInit {

  products: Product[] = [];
  sortedProducts: Product[] = [];
  productQuantities: Record<string, number> = {};

  sortKey: 'name' | 'sku' = 'name';
  sortAsc = true;

  // Modal
  showModal = false;
  selectedProduct?: Product;
  modalQuantity = 1;
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
      next: (products) => {
        this.products = products;
        this.products.forEach(p => this.productQuantities[p.id] = 1);
        this.sortProducts();
      },
      error: () => this.errorMessage = 'Failed to load products'
    });
  }

  toggleSort(key: 'name' | 'sku'): void {
    if (this.sortKey === key) {
      this.sortAsc = !this.sortAsc;
    } else {
      this.sortKey = key;
      this.sortAsc = true;
    }
    this.sortProducts();
  }

  sortProducts(): void {
    this.sortedProducts = [...this.products].sort((a, b) => {
      const valA = (a[this.sortKey] ?? '').toString().trim().toLowerCase();
      const valB = (b[this.sortKey] ?? '').toString().trim().toLowerCase();
      return this.sortAsc ? (valA > valB ? 1 : -1) : (valA < valB ? 1 : -1);
    });
  }

  openModal(product: Product): void {
    this.selectedProduct = product;
    this.modalQuantity = this.productQuantities[product.id] || 1;
    this.description = '';
    this.errorMessage = '';
    this.showModal = true;
  }

  closeModal(): void {
    this.showModal = false;
    this.selectedProduct = undefined;
    this.modalQuantity = 1;
    this.description = '';
    this.errorMessage = '';
  }

  placeOrder(): void {
    if (!this.selectedProduct) return;

    const order: OrderCreateRequest = {
      description: this.description || undefined,
      items: [
        { product_name: this.selectedProduct.name, quantity: this.modalQuantity }
      ]
    };

    this.loading = true;
    this.orderService.createOrder(order).subscribe({
      next: () => {
        this.loading = false;
        this.productQuantities[this.selectedProduct!.id] = this.modalQuantity;
        this.closeModal();
        alert('Order placed successfully!');
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err?.message || 'Failed to place order';
      }
    });
  }
}
