# System Architecture

## Übersicht

Das automatisierte Einkommens-Setup-System folgt einer Client-Server-Architektur mit Offline-First-Ansatz.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Android Client                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Presentation Layer                       │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Compose   │  │ ViewModels │  │ Navigation │     │   │
│  │  │     UI     │  │            │  │            │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Domain Layer                             │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Use Cases │  │   Models   │  │  Business  │     │   │
│  │  │            │  │            │  │    Logic   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Data Layer                               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ Repository │  │    Room    │  │  Retrofit  │     │   │
│  │  │            │  │  Database  │  │   Client   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend Server                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Layer                                │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │   Routes   │  │ Middleware │  │    Auth    │     │   │
│  │  │            │  │            │  │    (JWT)   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Service Layer                            │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │  Business  │  │Recommend.  │  │    Sync    │     │   │
│  │  │   Logic    │  │   Engine   │  │  Service   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Data Layer                               │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐     │   │
│  │  │ Repository │  │ PostgreSQL │  │   Redis    │     │   │
│  │  │            │  │            │  │  (Cache)   │     │   │
│  │  └────────────┘  └────────────┘  └────────────┘     │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │  External Services │
                    │  ┌──────────────┐  │
                    │  │     FCM      │  │
                    │  │ (Push Notif.)│  │
                    │  └──────────────┘  │
                    └────────────────────┘
```

## Komponenten-Details

### Android Client

#### Presentation Layer
- **Jetpack Compose:** Deklaratives UI Framework
- **ViewModels:** UI State Management, Lifecycle-aware
- **Navigation:** Screen Navigation mit Navigation Compose
- **Theme:** Material Design 3 Theme System

#### Domain Layer
- **Use Cases:** Geschäftslogik, wiederverwendbar
- **Models:** Domain-spezifische Datenmodelle
- **Validators:** Input-Validierung

#### Data Layer
- **Repository Pattern:** Single Source of Truth
- **Room Database:** Lokale SQLite-Datenbank
- **Retrofit:** REST API Client
- **WorkManager:** Background-Tasks für Sync

### Backend Server

#### API Layer
- **REST Endpoints:** RESTful API Design
- **Middleware:** Logging, Error Handling, CORS
- **Authentication:** JWT-basiert
- **Validation:** Request/Response Validation

#### Service Layer
- **Business Logic:** Kerngeschäftslogik
- **Recommendation Engine:** Empfehlungsalgorithmen
- **Sync Service:** Synchronisierungslogik

#### Data Layer
- **Repository Pattern:** Datenzugriffs-Abstraktion
- **PostgreSQL:** Relationale Datenbank
- **Redis:** Caching und Session Storage

### External Services
- **Firebase Cloud Messaging:** Push-Benachrichtigungen
- **Analytics:** User Tracking (optional)
- **Error Tracking:** Sentry (optional)

## Design Patterns

### Android

1. **MVVM (Model-View-ViewModel)**
   - View: Composables
   - ViewModel: UI State & Logic
   - Model: Data Layer

2. **Clean Architecture**
   - Presentation → Domain → Data
   - Dependency Rule: Inner layers don't know outer layers

3. **Repository Pattern**
   - Abstract data sources
   - Single source of truth

4. **Dependency Injection (Hilt)**
   - Loose coupling
   - Testability

### Backend

1. **Layered Architecture**
   - API → Service → Repository → Database

2. **Repository Pattern**
   - Data access abstraction

3. **Dependency Injection**
   - Service configuration

## Data Flow

### Create Income (Beispiel)

```
User Input (Compose UI)
  ↓
ViewModel.createIncome()
  ↓
CreateIncomeUseCase.execute()
  ↓
IncomeRepository.create()
  ├─→ Room: Save locally
  └─→ API: Sync to server (wenn online)
  ↓
Server API Endpoint
  ↓
Service Layer: Validate & Process
  ↓
Repository: Save to PostgreSQL
  ↓
Response to Client
  ↓
Update UI State
```

### Sync Flow (Offline → Online)

```
WorkManager (periodic/connectivity change)
  ↓
SyncWorker
  ↓
SyncRepository.syncPendingChanges()
  ├─→ Get local changes (Room)
  ├─→ Upload to server (API)
  ├─→ Get server changes
  └─→ Merge & resolve conflicts
  ↓
Update local database
  ↓
Notify UI (if app is active)
```

## Technology Decisions

### Warum Jetpack Compose?
- Modern, deklarativ
- Weniger Boilerplate
- Bessere Performance
- State Management eingebaut

### Warum Room?
- Type-safe SQL
- Compile-time verification
- LiveData/Flow support
- Offline-First

### Warum Hilt?
- Android-optimiert
- Einfachere DI als Dagger
- Lifecycle-aware

### Warum PostgreSQL?
- Robust, skalierbar
- JSON support
- ACID-compliant
- Gut für komplexe Queries

### Warum Redis?
- Schnelles Caching
- Session Storage
- Rate Limiting

## Security Architecture

### Authentifizierung
- JWT Tokens
- Refresh Token Rotation
- Secure Storage (Android Keystore)

### Datenverschlüsselung
- HTTPS/TLS für Transit
- Database Encryption at Rest
- Sensitive Data Encryption in App

### API Security
- Rate Limiting
- Input Validation
- SQL Injection Prevention
- XSS Prevention

## Scalability Considerations

### Horizontal Scaling
- Stateless API Server
- Load Balancer
- Database Replication

### Caching Strategy
- Redis für Sessions
- API Response Caching
- Client-side Caching (Room)

### Performance
- Database Indexing
- Query Optimization
- Lazy Loading
- Pagination

## Weitere Details

Siehe auch:
- [API Documentation](../api/README.md)
- [Android README](../../android/README.md)
- [Backend README](../../backend/README.md)
