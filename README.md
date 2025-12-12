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
- Python 3.11+
- Node.js 18+
- SQLite

### Installation

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

### Environment Variables

Copy `.env.example` to `.env` and configure:
- `SECRET_KEY`: Secret key for JWT
- `DATABASE_URL`: Database URL
- `ENCRYPTION_KEY`: Key to encrypt API keys
- `CORS_ORIGINS`: Allowed origins for CORS

## 🧪 Testing

The project follows a TDD (Test-Driven Development) approach:

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

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

[To be defined]

## 👥 Contributing

[To be defined]

## 📧 Contact

[To be defined]
