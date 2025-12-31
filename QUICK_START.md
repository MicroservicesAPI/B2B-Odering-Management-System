# B2B Ordering System - Quick Start Guide

This guide will help you get the complete B2B Ordering System (frontend + backend) up and running quickly.

## Prerequisites

### Backend Requirements
- Docker and Docker Compose
- Python 3.11+ (optional, for local development)

### Frontend Requirements
- Node.js v20.x or higher
- npm v10.x or higher
- Angular CLI 19.2.5 (will be installed with npm install)

## Quick Start - Full Stack

### Option 1: Using Docker (Backend Only) + Angular Dev Server

This is the recommended approach for development.

#### Step 1: Start Backend Services

```bash
# From project root
docker-compose up --build
```

This will start:
- API Gateway on port 8000
- Auth Service on port 8001
- Order Service on port 8002
- Product Service on port 8003

Wait for all services to start successfully. You should see logs indicating all services are running.

#### Step 2: Start Frontend

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend/b2b-ordering-app

# Install dependencies (first time only)
npm install

# Start development server with proxy
npm start
```

The Angular app will start on http://localhost:4200

#### Step 3: Access the Application

1. Open your browser and navigate to http://localhost:4200
2. You'll be redirected to the login page
3. Use test credentials to log in (see Test Users section below)

### Option 2: Local Development (All Services)

For advanced development where you want to run backend services locally without Docker:

#### Backend Services

```bash
# Terminal 1 - API Gateway
cd services/api-gateway
pip install -r requirements.txt
python run.py

# Terminal 2 - Auth Service
cd services/auth-service
pip install -r requirements.txt
LOCAL_RUN=1 python run.py

# Terminal 3 - Order Service
cd services/order-service
pip install -r requirements.txt
LOCAL_RUN=1 python run.py

# Terminal 4 - Product Service
cd services/product-service
pip install -r requirements.txt
LOCAL_RUN=1 python run.py
```

#### Frontend

```bash
# Terminal 5 - Frontend
cd frontend/b2b-ordering-app
npm install
npm start
```

## Test Users

After starting the backend, you can create test users via the API or use the following if seeded:

### Admin User
- **Email**: admin@company.com
- **Password**: admin123
- **Role**: ADMIN
- **Permissions**: Full access (create products, view all orders, etc.)

### Staff User
- **Email**: staff@company.com
- **Password**: staff123
- **Role**: STAFF
- **Permissions**: View products, manage own orders

**Note**: You may need to register these users first using the registration endpoint or the Auth Service directly.

## Creating Your First User

If no users exist, you can create one using the API:

### Using curl

```bash
# Register an admin user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@company.com",
    "password": "admin123",
    "role": "ADMIN"
  }'

# Register a staff user
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "staff@company.com",
    "password": "staff123",
    "role": "STAFF",
    "department_id": "your-department-id"
  }'
```

### Using API Docs

1. Navigate to http://localhost:8000/docs
2. Find the `/auth/register` endpoint
3. Click "Try it out"
4. Fill in the user details
5. Execute the request

## Verifying the Setup

### Backend Health Check

```bash
# Check API Gateway
curl http://localhost:8000/health

# Or visit in browser
http://localhost:8000/docs
```

### Frontend Access

1. Open http://localhost:4200
2. You should see the login page
3. Login form should be displayed properly
4. No console errors in browser developer tools

## Common Features to Test

### 1. Login
- Navigate to http://localhost:4200
- Enter credentials
- Click "Login"
- Should redirect to home page with product list

### 2. View Products (All Users)
- After login, you'll see the products page
- Products display with name, SKU, description, and stock levels
- Low stock items are highlighted

### 3. Create Product (Admin Only)
- Login as admin user
- Click "Create Product" in navbar
- Fill in product details
- Submit form
- Should redirect to home page with new product visible

### 4. View My Orders (All Users)
- Click "My Orders" in navbar
- View list of your orders
- See order status, items, and details

### 5. Logout
- Click "Logout" button in navbar
- Should redirect to login page
- Access token should be cleared

## Troubleshooting

### Frontend Cannot Connect to Backend

**Problem**: Frontend shows connection errors or API requests fail

**Solutions**:
1. Ensure backend services are running (check Docker logs)
2. Verify API Gateway is accessible: http://localhost:8000/docs
3. Check proxy configuration in `frontend/b2b-ordering-app/proxy.conf.json`
4. Check browser console for CORS errors
5. Restart the Angular dev server

### Login Fails

**Problem**: Login returns 401 or credentials error

**Solutions**:
1. Verify user exists in the database
2. Check Auth Service logs for errors
3. Ensure password is correct
4. Try registering a new user first

### Products Not Loading

**Problem**: Home page shows "Failed to load products"

**Solutions**:
1. Ensure Product Service is running
2. Check that you're logged in (JWT token is valid)
3. Verify API Gateway can reach Product Service
4. Create some test products using the API

### Build Errors

**Problem**: `npm install` or `npm start` fails

**Solutions**:
1. Verify Node.js version: `node --version` (should be v20.x+)
2. Verify npm version: `npm --version` (should be v10.x+)
3. Clear npm cache: `npm cache clean --force`
4. Delete `node_modules` and `package-lock.json`, then run `npm install` again
5. Check for port conflicts (port 4200 should be free)

### Docker Issues

**Problem**: Docker containers won't start

**Solutions**:
1. Check Docker is running: `docker ps`
2. Check for port conflicts: `docker-compose down` then `docker-compose up`
3. View logs: `docker-compose logs -f [service-name]`
4. Rebuild: `docker-compose up --build --force-recreate`

## Development Tips

### Hot Reload

- **Frontend**: Angular dev server automatically reloads on file changes
- **Backend**: FastAPI with `--reload` flag reloads on code changes

### API Testing

Use the Swagger UI at http://localhost:8000/docs to:
- Test API endpoints
- View request/response schemas
- Generate authentication tokens
- Explore available operations

### Browser Developer Tools

- Open DevTools (F12)
- Check Console tab for errors
- Check Network tab to see API requests
- Check Application > Local Storage to see JWT tokens

### Code Structure

```
Project Root
├── services/           # Backend microservices
│   ├── api-gateway/   # API Gateway (port 8000)
│   ├── auth-service/  # Auth Service (port 8001)
│   ├── order-service/ # Order Service (port 8002)
│   └── product-service/ # Product Service (port 8003)
└── frontend/          # Frontend application
    └── b2b-ordering-app/  # Angular application
```

## Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Create Products**: Use the admin account to add products
3. **Create Orders**: Use the staff account to create orders
4. **Customize**: Modify the frontend components to match your needs
5. **Deploy**: Follow deployment guides for production setup

## Getting Help

- **Backend Issues**: Check service logs in Docker
- **Frontend Issues**: Check browser console and Angular terminal output
- **API Issues**: Use Swagger UI at http://localhost:8000/docs
- **Documentation**: Review README files in service directories

## Useful Commands

```bash
# Backend
docker-compose up -d          # Start in background
docker-compose down           # Stop all services
docker-compose logs -f        # View logs
docker-compose restart        # Restart services

# Frontend
npm start                     # Start dev server
npm run build                 # Production build
npm test                      # Run tests

# Clean up
docker-compose down -v        # Stop and remove volumes
rm -rf node_modules           # Remove frontend dependencies
```

## Production Deployment

For production deployment:

1. Build the frontend: `cd frontend/b2b-ordering-app && npm run build`
2. Deploy the `dist/` directory to a web server (Nginx, Apache, etc.)
3. Deploy backend services using Docker or container orchestration
4. Configure environment variables for production
5. Set up proper database (PostgreSQL)
6. Enable HTTPS/SSL
7. Configure proper CORS settings
8. Set up monitoring and logging

---

**Happy coding!** 🚀
