import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { ProductCreateRequest } from '../../models/product.model';

@Component({
  selector: 'app-product-create',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-create.component.html',
  styleUrl: './product-create.component.scss'
})
export class ProductCreateComponent {
  product: ProductCreateRequest = {
    name: '',
    sku: '',
    description: '',
    stock_quantity: 0,
    min_stock: 0
  };
  errorMessage = '';
  successMessage = '';
  loading = false;

  constructor(
    private productService: ProductService,
    private router: Router
  ) {}

  onSubmit(): void {
    if (!this.validateForm()) {
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.productService.createProduct(this.product).subscribe({
      next: (response) => {
        this.loading = false;
        this.successMessage = 'Product created successfully!';
        setTimeout(() => {
          this.router.navigate(['/home']);
        }, 1500);
      },
      error: (error) => {
        this.loading = false;
        this.errorMessage = error.error?.detail || 'Failed to create product. Please try again.';
      }
    });
  }

  validateForm(): boolean {
    if (!this.product.name || !this.product.sku || !this.product.description) {
      this.errorMessage = 'Please fill in all required fields';
      return false;
    }

    if (this.product.stock_quantity < 0 || this.product.min_stock < 0) {
      this.errorMessage = 'Stock quantities cannot be negative';
      return false;
    }

    return true;
  }

  resetForm(): void {
    this.product = {
      name: '',
      sku: '',
      description: '',
      stock_quantity: 0,
      min_stock: 0
    };
    this.errorMessage = '';
    this.successMessage = '';
  }
}
