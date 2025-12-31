# B2B Ordering System - Frontend

This is the Angular frontend for the B2B Ordering Management System.

## Technology Stack

- **Angular**: 19.2.5
- **TypeScript**: Latest
- **SCSS**: For styling
- **Node.js**: v20.x
- **npm**: 10.8.2

## Features

### Authentication
- Login page with form validation
- JWT token-based authentication
- Auto-redirect to login for protected routes
- Logout functionality

### Product Management
- View all available products (Home page)
- Product creation (Admin only)
- Display stock levels with visual indicators
- Low stock warnings

### Order Tracking
- View user's orders (My Orders page)
- Display order status (Pending, Approved, Rejected, Delivered)
- Show order details and items
- Track order history

### Navigation
- Responsive navbar
- Role-based menu items (Admin sees additional options)
- User information display
- Active route highlighting

## Getting Started

### Prerequisites

- Node.js (v20.x or higher)
- npm (v10.x or higher)
- API Gateway running on port 8000

### Installation

```bash
# Navigate to the frontend directory
cd frontend/b2b-ordering-app

# Install dependencies
npm install
```

### Running the Application

#### Development Server

```bash
# Run with proxy configuration (recommended)
npm start

# Or manually with proxy
ng serve --proxy-config proxy.conf.json
```

The application will be available at `http://localhost:4200`

#### Production Build

```bash
# Build for production
npm run build

# The build artifacts will be in the dist/ directory
```

### Proxy Configuration

The application uses a proxy configuration (`proxy.conf.json`) to forward API requests to the backend API Gateway running on port 8000. This avoids CORS issues during development.

## Project Structure

```
src/
├── app/
│   ├── components/          # UI Components
│   │   ├── login/          # Login page
│   │   ├── home/           # Products list page
│   │   ├── product-create/ # Product creation form
│   │   ├── my-orders/      # User orders page
│   │   └── navbar/         # Navigation bar
│   ├── guards/             # Route guards
│   │   └── auth.guard.ts   # Authentication & authorization guards
│   ├── interceptors/       # HTTP interceptors
│   │   └── auth.interceptor.ts  # JWT token interceptor
│   ├── models/             # TypeScript interfaces
│   │   ├── user.model.ts
│   │   ├── product.model.ts
│   │   └── order.model.ts
│   ├── services/           # API services
│   │   ├── auth.service.ts
│   │   ├── product.service.ts
│   │   └── order.service.ts
│   ├── app.component.*     # Root component
│   ├── app.config.ts       # Application configuration
│   └── app.routes.ts       # Routing configuration
├── styles.scss             # Global styles
└── index.html             # Main HTML file
```

## Routes

| Route | Component | Access | Description |
|-------|-----------|--------|-------------|
| `/login` | LoginComponent | Public | User login |
| `/home` | HomeComponent | Authenticated | View products |
| `/my-orders` | MyOrdersComponent | Authenticated | View user orders |
| `/product-create` | ProductCreateComponent | Admin only | Create new product |

## API Integration

The frontend integrates with the following backend services through the API Gateway:

- **Auth Service** (`/auth/*`): User authentication and authorization
- **Product Service** (`/products/*`): Product management
- **Order Service** (`/orders/*`): Order management

All requests include JWT tokens via the HTTP interceptor for authenticated endpoints.

## User Roles

- **ADMIN**: Full access to all features including product creation
- **STAFF**: Access to view products and manage their own orders

## Development Notes

### Authentication Flow

1. User submits credentials via login form
2. Frontend sends POST request to `/auth/login`
3. Backend returns JWT tokens and user info
4. Tokens stored in localStorage
5. HTTP interceptor adds token to all subsequent requests
6. Route guards protect authenticated routes

### Guard Usage

- `authGuard`: Ensures user is authenticated
- `adminGuard`: Ensures user has ADMIN role

### Styling

- Uses SCSS for component-specific and global styles
- Responsive design principles
- Color-coded status indicators
- Hover effects and animations

## Testing

```bash
# Run unit tests
npm test

# Run end-to-end tests
npm run e2e
```

## Building for Production

```bash
# Build the application
npm run build

# The output will be in dist/b2b-ordering-app/browser/
```

## Environment Configuration

The application currently uses hardcoded API endpoints via proxy. For production:

1. Update service URLs to point to production API Gateway
2. Configure environment files for different environments
3. Use Angular environment configuration

## Troubleshooting

### Cannot connect to backend

- Ensure API Gateway is running on port 8000
- Check proxy configuration in `proxy.conf.json`
- Verify CORS settings on backend

### Authentication issues

- Clear localStorage and try logging in again
- Check JWT token expiration
- Verify backend auth service is running

### Build errors

- Delete `node_modules` and run `npm install` again
- Clear Angular cache: `rm -rf .angular`
- Ensure using correct Node.js and npm versions

## Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## License

This project is part of the B2B Ordering Management System.
