# Backend API

Dieses Verzeichnis enthält die Backend-API für das automatisierte Einkommens-Setup-Projekt.

## Technologie-Stack (zur Auswahl)

### Option 1: FastAPI (Python)
- **Framework:** FastAPI
- **Datenbank:** PostgreSQL (asyncpg)
- **ORM:** SQLAlchemy 2.0
- **Migration:** Alembic
- **Validation:** Pydantic V2
- **Auth:** JWT (python-jose)
- **Testing:** pytest

### Option 2: Express.js (Node.js)
- **Framework:** Express.js
- **Datenbank:** PostgreSQL (pg)
- **ORM:** Prisma/TypeORM
- **Migration:** Prisma Migrate
- **Validation:** Zod/Joi
- **Auth:** JWT (jsonwebtoken)
- **Testing:** Jest/Mocha

### Option 3: Ktor (Kotlin)
- **Framework:** Ktor
- **Datenbank:** PostgreSQL (Exposed)
- **ORM:** Exposed
- **Validation:** Kotlinx Serialization
- **Auth:** JWT
- **Testing:** Kotlin Test

## API Struktur

```
backend/
├── src/
│   ├── api/              # API Endpoints
│   │   ├── routes/       # Route Handlers
│   │   └── middleware/   # Middleware
│   ├── core/             # Core Configuration
│   │   ├── config.py/ts  # Configuration
│   │   ├── database.py/ts # Database Setup
│   │   └── security.py/ts # Auth & Security
│   ├── models/           # Database Models
│   ├── schemas/          # Request/Response Schemas
│   ├── services/         # Business Logic
│   ├── repositories/     # Data Access Layer
│   └── utils/            # Utilities
├── tests/                # Tests
├── migrations/           # Database Migrations
├── requirements.txt      # Python Dependencies
├── package.json          # Node.js Dependencies
├── Dockerfile            # Docker Configuration
└── docker-compose.yml    # Docker Compose
```

## Setup

### Mit Docker (empfohlen)

```bash
docker-compose up -d
```

### Lokal (Python/FastAPI)

```bash
# Virtual Environment erstellen
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Dependencies installieren
pip install -r requirements.txt

# Datenbank Migrationen
alembic upgrade head

# Server starten
uvicorn src.main:app --reload
```

### Lokal (Node.js/Express)

```bash
# Dependencies installieren
npm install

# Datenbank Migrationen
npx prisma migrate dev

# Server starten
npm run dev
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Nutzer registrieren
- `POST /api/auth/login` - Login
- `POST /api/auth/logout` - Logout
- `POST /api/auth/refresh` - Token erneuern

### Users
- `GET /api/users/me` - Aktueller Nutzer
- `PUT /api/users/me` - Profil aktualisieren
- `DELETE /api/users/me` - Account löschen

### Income
- `GET /api/income` - Alle Einkommensquellen
- `POST /api/income` - Neue Einkommensquelle
- `GET /api/income/{id}` - Einzelne Quelle
- `PUT /api/income/{id}` - Quelle aktualisieren
- `DELETE /api/income/{id}` - Quelle löschen

### Recommendations
- `GET /api/recommendations` - Empfehlungen abrufen
- `POST /api/recommendations/feedback` - Feedback senden

### Sync
- `GET /api/sync/status` - Sync-Status
- `GET /api/sync/changes` - Änderungen abrufen
- `POST /api/sync/push` - Änderungen hochladen

## Datenbank

### PostgreSQL Setup

```bash
# Docker
docker run --name sabsteck-db \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=sabsteckapi \
  -p 5432:5432 \
  -d postgres:14

# Verbindung
postgresql://postgres:password@localhost:5432/sabsteckapi
```

### Migrationen

```bash
# Python/Alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Node.js/Prisma
npx prisma migrate dev --name init
```

## Tests

```bash
# Python/pytest
pytest
pytest --cov=src --cov-report=html

# Node.js/Jest
npm test
npm run test:coverage
```

## Dokumentation

API-Dokumentation ist automatisch verfügbar unter:

- **FastAPI:** http://localhost:8000/docs (Swagger UI)
- **Express:** http://localhost:3000/api-docs (falls konfiguriert)

## Umgebungsvariablen

Erstellen Sie eine `.env` Datei:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/sabsteckapi

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080

# Redis (optional)
REDIS_URL=redis://localhost:6379
```

## Deployment

Siehe [DEPLOYMENT.md](../docs/DEPLOYMENT.md)

## Weitere Informationen

Siehe [Hauptdokumentation](../PROJECT.md)
