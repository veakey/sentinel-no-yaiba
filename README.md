# Sentinel no Yaiba

<div align="center">
  <img src="docs/assets/logo.png" alt="Sentinel no Yaiba Logo" width="200"/>
  
  **Unified security dashboard for threat intelligence aggregation**
</div>

## 📋 Description

Sentinel no Yaiba is a full-stack application that aggregates threat intelligence data from multiple security providers (Ninja One, Malwarebytes, etc.) via their APIs. The application provides a unified dashboard to visualize and analyze this data in a centralized manner.

### 🎯 Main Objectives

- **Multi-source aggregation**: Collect data from multiple security providers via their APIs
- **Unified visualization**: Centralized dashboard to visualize all detected threats
- **Extensibility**: Modular architecture allowing easy integration of new providers
- **Real-time updates**: Automatic updates via WebSocket when new data is available
- **Permission management**: Role-based system (Admin/Client) to control access to features

## 🏗️ Architecture

### Technology Stack

**Backend**
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Cache**: Multi-level system (memory + SQLite)
- **Authentication**: JWT with roles and permissions
- **WebSocket**: FastAPI WebSocket for real-time updates
- **Tests**: pytest (unit, integration, functional)

**Frontend**
- **Framework**: React with TypeScript
- **Build tool**: Vite
- **Tests**: Vitest + React Testing Library
- **Visualizations**: Recharts (or similar library)

### Provider Architecture

The system uses a Factory pattern to manage different providers in an extensible way:

```
BaseProvider (abstract interface)
├── NinjaProvider
├── MalwarebytesProvider
└── [Future providers...]
```

## 🔑 Features

### For Administrators
- ✅ Provider configuration (add, modify, enable/disable)
- ✅ User and permission management
- ✅ Custom dashboard configuration
- ✅ Audit log consultation
- ✅ Full access to all features

### For Clients
- ✅ View public and assigned dashboards
- ✅ Consult threat intelligence data in real-time
- ✅ Automatic updates via WebSocket
- ✅ Search and filter threats

### Technical Features
- **Smart caching**: Instant responses for previously executed queries, with asynchronous refresh
- **Unique GUID**: All entities expose a GUID for external identification (security)
- **Encryption**: API keys encrypted in database
- **Rate limiting**: Protection against API abuse
- **Audit logging**: Complete traceability of administrative actions
- **Health checks**: Endpoints for monitoring

## 📦 Supported Providers

- **Ninja One**: Endpoint monitoring and management
- **Malwarebytes**: Threat detection and prevention
- *More providers coming soon...*

See [docs/api-links.md](docs/api-links.md) for API documentation links.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ (Python 3.13 supported)
- Node.js 18+ (for frontend, not yet implemented)
- SQLite (included with Python)

### Backend Setup

1. **Navigate to backend directory:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
python -m pip install -r requirements.txt
```

3. **Create environment file:**
```bash
# Windows PowerShell
Copy-Item .env.example .env

# Windows CMD
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

   **Note:** While default values are provided in code for development, creating a `.env` file is recommended for proper configuration. The `.env.example` file contains all required variables with default values.

4. **Configure environment variables (optional for development):**
   
   For development, the default values in `.env.example` work out of the box. For production, edit the `.env` file and update:
   - `SECRET_KEY`: Secret key for JWT (default: works for dev)
   - `DATABASE_URL`: Database URL (default: `sqlite:///./sentinel.db`)
   - `CORS_ORIGINS`: Allowed origins for CORS (default: `http://localhost:3000,http://localhost:5173`)
   - `ENCRYPTION_KEY`: Key to encrypt API keys (optional)

5. **Initialize admin user:**
```bash
# Option 1: From the project root
python backend/scripts/init_admin.py

# Option 2: From the backend directory
cd backend
python scripts/init_admin.py
```

   This creates a default admin user with:
   - Username: `admin`
   - Password: `admin123`
   - Email: `admin@example.com`

   To create a custom admin user:
```bash
# From the project root
python backend/scripts/init_admin.py --username monadmin --password monpassword --email monadmin@example.com

# Or from the backend directory
cd backend
python scripts/init_admin.py --username monadmin --password monpassword --email monadmin@example.com
```

   **Note:** If the admin user already exists, the script will inform you. You can still use the existing credentials or create a new admin with different credentials.

6. **Run the application:**
```bash
# From the backend directory
python -m uvicorn app.main:app --reload
```

The API will be available at:
- API: http://127.0.0.1:8000
- Documentation: http://127.0.0.1:8000/api/docs
- ReDoc: http://127.0.0.1:8000/api/redoc

### Frontend Setup

*Frontend setup will be available soon*

## 🧪 Testing

The project follows a TDD (Test-Driven Development) approach:

### Backend Tests

```bash
# From the backend directory
cd backend
python -m pytest -v

# Run specific test file
python -m pytest tests/test_config.py -v

# Run with coverage
python -m pytest --cov=app --cov-report=term-missing
```

**Note:** Tests work without a `.env` file as default values are provided. The `.env.example` file is used as a template for production configuration.

### Frontend Tests

*Frontend tests will be available when frontend is implemented*

## 📚 Project Structure

```
sentinel-no-yaiba/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── auth/         # JWT authentication
│   │   ├── cache/        # Cache manager
│   │   ├── core/         # Utilities (config, exceptions, etc.)
│   │   ├── database/     # DB models and migrations
│   │   ├── providers/    # Provider implementations
│   │   ├── services/     # Business logic
│   │   └── websocket/    # WebSocket manager
│   └── tests/            # Backend tests
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── contexts/     # Contexts (Auth, WebSocket)
│   │   ├── hooks/        # Custom hooks
│   │   ├── services/     # API services
│   │   └── types/        # TypeScript types
│   └── tests/            # Frontend tests
└── docs/                 # Documentation
```

## 🔒 Security

- API keys encrypted in database
- JWT authentication with refresh tokens
- Server-side input validation
- Configured CORS
- Rate limiting on endpoints
- Audit logging of sensitive actions

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributing

[To be defined]

## 📧 Contact

[To be defined]
