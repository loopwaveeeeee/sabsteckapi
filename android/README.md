# Android App

Dieses Verzeichnis enthält die Android App für das automatisierte Einkommens-Setup-Projekt.

## Technologie-Stack

- **Sprache:** Kotlin
- **UI Framework:** Jetpack Compose
- **Architecture:** MVVM + Clean Architecture
- **Dependency Injection:** Hilt
- **Lokale Datenbank:** Room
- **Networking:** Retrofit + OkHttp
- **Async:** Coroutines + Flow
- **Navigation:** Navigation Compose

## Struktur

```
android/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/sabsteck/incomesetup/
│   │   │   │   ├── data/           # Data Layer
│   │   │   │   │   ├── local/      # Room Database, DAOs
│   │   │   │   │   ├── remote/     # API Services
│   │   │   │   │   └── repository/ # Repositories
│   │   │   │   ├── domain/         # Domain Layer
│   │   │   │   │   ├── model/      # Domain Models
│   │   │   │   │   └── usecase/    # Use Cases
│   │   │   │   ├── di/             # Dependency Injection
│   │   │   │   ├── ui/             # Presentation Layer
│   │   │   │   │   ├── screens/    # Composable Screens
│   │   │   │   │   ├── components/ # Reusable Components
│   │   │   │   │   ├── navigation/ # Navigation
│   │   │   │   │   └── theme/      # Theme, Colors, Typography
│   │   │   │   └── util/           # Utilities
│   │   │   └── res/                # Resources
│   │   └── test/                   # Unit Tests
│   └── build.gradle.kts
├── gradle/
├── build.gradle.kts
└── settings.gradle.kts
```

## Setup

### Voraussetzungen
- Android Studio Arctic Fox oder neuer
- JDK 17+
- Android SDK 24+ (Minimum API Level)
- Android SDK 34+ (Target API Level)

### Installation

1. Projekt in Android Studio öffnen
2. Gradle Sync durchführen
3. App auf Emulator oder Gerät starten

```bash
./gradlew build
```

## Entwicklung

### Build Variants
- `debug` - Entwicklungsversion
- `release` - Produktionsversion

### Tests ausführen

```bash
# Unit Tests
./gradlew test

# Instrumented Tests
./gradlew connectedAndroidTest

# Alle Tests
./gradlew check
```

### Code Style

Das Projekt verwendet ktlint für Kotlin Code Formatting.

```bash
# Formatierung prüfen
./gradlew ktlintCheck

# Automatisch formatieren
./gradlew ktlintFormat
```

## Architektur

### MVVM + Clean Architecture

```
UI Layer (Composables)
    ↓
ViewModel
    ↓
Use Cases (Domain)
    ↓
Repository (Data)
    ↓
Data Sources (Local/Remote)
```

### Dependency Injection mit Hilt

Module sind in `di/` organisiert:
- `AppModule` - App-weite Dependencies
- `DatabaseModule` - Room Database
- `NetworkModule` - Retrofit, OkHttp
- `RepositoryModule` - Repositories

## Features

- [ ] User Authentication
- [ ] Income Tracking
- [ ] Dashboard
- [ ] Recommendations
- [ ] Settings
- [ ] Offline Mode
- [ ] Synchronization

## Weitere Informationen

Siehe [Hauptdokumentation](../PROJECT.md)
