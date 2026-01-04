import { Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { HomeComponent } from './components/home/home.component';
import { ProductCreateComponent } from './components/product-create/product-create.component';
import { MyOrdersComponent } from './components/my-orders/my-orders.component';
import {DocumentationComponent} from "./components/documentation/documentation.component";
import { authGuard, adminGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: 'login', component: LoginComponent },

  { path: 'home', component: HomeComponent, canActivate: [authGuard] },

  { path: 'documentation', component: DocumentationComponent, canActivate: [authGuard] },

  { path: 'my-orders', component: MyOrdersComponent, canActivate: [authGuard] },

      // -----------------------------------------------------
  // Moderne Variante: Lazy Load einer Standalone-Komponente

  {
    path: 'make-order',
    canActivate: [authGuard],
    loadComponent: () =>
      import('./components/make-order/make-order.component')
        .then(m => m.MakeOrderComponent)
  },
          // -----------------------------------------------------
    //  Klassische Variante: Component direkt referenzieren

  {
    path: 'product-create',
    component: ProductCreateComponent,
    canActivate: [authGuard, adminGuard]
  },

  { path: '', redirectTo: '/home', pathMatch: 'full' },

  { path: '**', redirectTo: '/home' }
];


