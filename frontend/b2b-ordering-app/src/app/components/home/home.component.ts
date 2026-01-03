import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../services/product.service';
import { Product } from '../../models/product.model';
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-home',
  standalone: true,
    imports: [CommonModule, RouterLink],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  products: Product[] = [];
  loading = false;
  errorMessage = '';

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.loading = true;
    this.errorMessage = '';

    this.productService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.loading = false;
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = 'Failed to load products. Please try again later.';
        console.error('Error loading products:', error);
      }
    });
  }

  isLowStock(product: Product): boolean {
    return product.stock_quantity <= product.min_stock;
  }
}
