# DICT Procurement Management System

**Comprehensive Government Procurement System for the Department of Information and Communications Technology (DICT), Philippines**

Fully compliant with **RA 9184 - Government Procurement Reform Act** and **COA (Commission on Audit)** regulations.

---

## 🏗️ Architecture Overview

### Technology Stack

**Backend:**
- **Framework**: FastAPI 0.115+ (Python 3.12+)
- **Database**: MySQL 8.0+ (UTF8MB4, InnoDB)
- **ORM**: SQLAlchemy 2.0+ (async with aiomysql)
- **Authentication**: JWT + python-jose + passlib + bcrypt (cost factor 12)
- **Validation**: Pydantic 2.0+
- **Task Queue**: Celery 5.4+ + Redis
- **Migrations**: Alembic

**Frontend:**
- **Framework**: Vue.js 3 + TypeScript
- **State Management**: Pinia
- **Build Tool**: Vite
- **Styling**: Tailwind CSS

**DevOps:**
- **Containerization**: Docker 24+ + Docker Compose
- **Code Quality**: Ruff, mypy, pre-commit
- **Testing**: Pytest 7+ + pytest-asyncio

---

## 🚀 Quick Start

### Prerequisites

1. **Python 3.12+**
2. **MySQL 8.0+**
3. **Redis** (for Celery)
4. **Git**

### Setup Instructions

#### 1. Clone Repository

```bash
git clone <repository-url>
cd fastAPI
```

#### 2. Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your configuration:
# - Database credentials
# - JWT secret key (generate with: openssl rand -hex 32)
# - Redis connection
# - Email settings
```

**Critical Configuration:**
```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=dict_procurement
DATABASE_USER=root
DATABASE_PASSWORD=your_password_here

# JWT Secret (CHANGE THIS IN PRODUCTION!)
SECRET_KEY=your-secret-key-here-use-openssl-rand-hex-32
```

#### 4. Setup Database

```bash
# Create database
mysql -u root -p
CREATE DATABASE dict_procurement CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# Initialize Alembic
python scripts/init_alembic.py

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

#### 5. Run Application

```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python app/main.py
```

#### 6. Access API

- **API Documentation**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 🐳 Docker Deployment

### Using Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Services Included

1. **MySQL 8.0** - Database
2. **Redis** - Cache and message broker
3. **FastAPI App** - Main application
4. **Celery Worker** - Background tasks
5. **Celery Beat** - Scheduled tasks
6. **Nginx** - Reverse proxy (production only)

---

## 📊 Database Schema

### Core Tables (15)

1. **users** - User accounts with roles
2. **purchase_requests** - Main procurement requests
3. **pr_items** - Items within purchase requests
4. **rfqs** - Requests for quotation
5. **suppliers** - Registered suppliers
6. **canvasses** - Canvassing tasks
7. **supplier_quotations** - Supplier price quotations
8. **quotation_items** - Items within quotations
9. **quotation_images** - Supporting documents for quotations
10. **bac_documents** - BAC preparation documents
11. **approval_routings** - Sequential approval workflows
12. **purchase_orders** - Final purchase orders
13. **documents** - General file uploads
14. **activity_logs** - Comprehensive audit trail
15. **notifications** - In-app notifications

### Key Features

- **UTF8MB4** character set for full Unicode support
- **InnoDB** with ROW_FORMAT=DYNAMIC
- **Composite indexes** for performance
- **Foreign key constraints** for data integrity
- **JSON columns** for flexible data storage

---

## 👥 User Roles (8 Types)

| Role | Description | Permissions |
|------|-------------|-------------|
| **END_USER** | Regular employees | Create/manage own PRs |
| **PROCUREMENT_OFFICER** | Procurement staff | Review PRs, create RFQs |
| **CANVASSER** | Price canvassers | Create supplier quotations |
| **BAC_SECRETARIAT** | BAC admin staff | Prepare BAC documents |
| **BAC_MEMBER** | BAC committee member | Approve BAC documents |
| **BAC_CHAIR** | BAC committee head | Final approval authority |
| **SUPPLIER** | External suppliers | View/accept POs |
| **ADMIN** | System administrator | Full system access |

---

## 🔄 Complete Procurement Workflow

### 8-Stage Process

```
1. PR Creation
   Status: PR_UNDER_REVIEW
   Action: END_USER creates PR with items

2. PR Approval Routing
   Status: RFQ_READY
   Action: Sequential approval by designated approvers

3. RFQ Creation
   Status: RFQ_DISSEMINATED
   Action: PROCUREMENT_OFFICER creates RFQ from approved PR

4. Canvassing
   Status: CANVASS_COMPLETE
   Action: CANVASSER collects supplier quotations

5. BAC Documents
   Status: BAC_APPROVED
   Action: BAC_SECRETARIAT prepares docs, BAC approves

6. Purchase Order
   Status: PO_APPROVED
   Action: PROCUREMENT_OFFICER generates PO

7. Supplier Conforme
   Status: AWAITING_CONFORME
   Action: SUPPLIER accepts/rejects PO

8. COA Stamping
   Status: COA_STAMPED
   Action: Final completion and COA stamp
```

---

## 🔐 Security Features

### Authentication & Authorization

- **JWT tokens** with configurable expiration (default: 2 hours)
- **bcrypt password hashing** (cost factor 12)
- **Password requirements**: 12+ chars, mixed case, numbers, symbols
- **Rate limiting**: 5 login attempts/minute, 15-minute lockout
- **Role-based access control** (RBAC) on all endpoints
- **Session timeout** after 2 hours of inactivity

### Data Protection

- **SQL injection prevention** via parameterized queries
- **XSS protection** via output encoding
- **CORS protection** for API endpoints
- **File upload validation** (magic numbers, size limits)
- **Audit logging** for all system actions
- **SSL/TLS** encryption in transit (production)

---

## 📡 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/password/reset` - Request password reset

### Purchase Requests
- `GET /api/v1/purchase-requests` - List PRs (paginated, filtered)
- `POST /api/v1/purchase-requests` - Create PR
- `GET /api/v1/purchase-requests/{id}` - Get PR details
- `PUT /api/v1/purchase-requests/{id}` - Update PR
- `DELETE /api/v1/purchase-requests/{id}` - Delete PR
- `POST /api/v1/purchase-requests/{id}/route` - Route for approval
- `POST /api/v1/purchase-requests/{id}/pdf` - Generate PDF

### RFQs
- `GET /api/v1/rfqs` - List RFQs
- `POST /api/v1/rfqs` - Create RFQ from PR
- `GET /api/v1/rfqs/{id}` - Get RFQ details
- `PUT /api/v1/rfqs/{id}` - Update RFQ
- `POST /api/v1/rfqs/{id}/activate` - Activate RFQ

### Approvals
- `GET /api/v1/approvals/pending` - List pending approvals
- `POST /api/v1/approvals/{id}/approve` - Approve document
- `POST /api/v1/approvals/{id}/reject` - Reject document
- `GET /api/v1/approvals/history` - Approval history

### ... and more

See `/api/docs` for complete interactive API documentation.

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

### Test Structure

```
tests/
├── unit/           # Unit tests (models, services, validators)
├── integration/    # Integration tests (API endpoints)
├── e2e/           # End-to-end tests (complete workflows)
└── fixtures/      # Test data fixtures
```

---

## 📈 Monitoring & Logging

### Application Logs

- **Location**: `logs/app.log`
- **Format**: JSON-structured logs
- **Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL

### Activity Logs (Database)

All major actions logged:
- User authentication (login, logout, password reset)
- CRUD operations (create, update, delete)
- Status changes
- Approvals/rejections
- Document uploads

---

## 🔧 Maintenance

### Database Backups

```bash
# Backup database
mysqldump -u root -p dict_procurement > backup_$(date +%Y%m%d).sql

# Restore database
mysql -u root -p dict_procurement < backup_20250113.sql
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Clear Cache (Redis)

```bash
# Clear all cache
redis-cli FLUSHALL

# Clear specific database
redis-cli -n 0 FLUSHDB
```

---

## 🤝 Contributing

### Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -am "Add feature"`
3. Run tests: `pytest`
4. Push branch: `git push origin feature/your-feature`
5. Create pull request

### Code Style

- **Linting**: `ruff check app/`
- **Type checking**: `mypy app/`
- **Format**: `ruff format app/`

---

## 📝 License

[Your License Here]

---

## 👨‍💻 Support

For issues, questions, or contributions:
- **Email**: support@dict.gov.ph
- **Documentation**: [Wiki/Docs URL]
- **Issue Tracker**: [GitHub Issues]

---

## 🙏 Acknowledgments

- Department of Information and Communications Technology (DICT)
- Republic Act 9184 - Government Procurement Reform Act
- Commission on Audit (COA)

---

**Built with ❤️ for the Philippine Government**
