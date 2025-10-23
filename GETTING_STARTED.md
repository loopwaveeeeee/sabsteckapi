# Getting Started Guide

Willkommen beim automatisierten Einkommens-Setup-Projekt! Dieses Dokument hilft Ihnen, schnell zu starten.

## 🎯 Projektziele

Entwicklung einer Android-App mit Backend-API zur automatisierten Verwaltung und Optimierung von Einkommensströmen.

## 📁 Projekt-Navigation

### Hauptdokumentation
- **[README.md](README.md)** - Projekt-Übersicht und Schnellstart
- **[PROJECT.md](PROJECT.md)** - Detaillierte Projektbeschreibung, Module und Meilensteine
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Wie Sie zum Projekt beitragen können

### Technische Dokumentation
- **[Architecture](docs/architecture/README.md)** - System-Architektur und Design-Patterns
- **[API Documentation](docs/api/README.md)** - REST API Endpoints und Schemas
- **[Deployment Guide](docs/DEPLOYMENT.md)** - Deployment-Prozess und Cloud-Konfiguration

### Komponenten
- **[Android App](android/README.md)** - Android-spezifische Dokumentation
- **[Backend API](backend/README.md)** - Backend-spezifische Dokumentation

### GitHub-Konfiguration
- **[Issue Templates](.github/ISSUE_TEMPLATE/)** - Vorlagen für Issues (9 Module + Bug/Feature)
- **[Milestones](.github/MILESTONES.md)** - MVP, V1.0, V1.1 Definitionen
- **[CI/CD Workflow](.github/workflows/ci.yml)** - Automatisierte Build & Test Pipeline

## 🚀 Schnellstart

### Für Entwickler

1. **Repository klonen**
   ```bash
   git clone https://github.com/loopwaveeeeee/sabsteckapi.git
   cd sabsteckapi
   ```

2. **Lesen Sie die Dokumentation**
   - Beginnen Sie mit [PROJECT.md](PROJECT.md)
   - Lesen Sie [CONTRIBUTING.md](CONTRIBUTING.md)

3. **Wählen Sie Ihren Bereich**
   - **Android:** Siehe [android/README.md](android/README.md)
   - **Backend:** Siehe [backend/README.md](backend/README.md)
   - **Design:** Siehe Issue Templates

### Für Product Owner / Project Manager

1. **Verstehen Sie die Meilensteine**
   - Lesen Sie [MILESTONES.md](.github/MILESTONES.md)
   - MVP: Basisfunktionen (6-8 Wochen)
   - V1.0: Produktionsreif (14-18 Wochen)

2. **Erstellen Sie Issues**
   - Nutzen Sie die [Issue Templates](.github/ISSUE_TEMPLATE/)
   - 9 module-spezifische Templates verfügbar
   - Bug Report & Feature Request Templates

3. **Planen Sie Sprints**
   - Verwenden Sie GitHub Projects
   - Organisieren Sie Issues nach Milestones
   - Weisen Sie Tasks zu

### Für Designer

1. **UX/Product Design**
   - Erstellen Sie Issues mit [UX Design Template](.github/ISSUE_TEMPLATE/01-ux-design.md)
   - Definieren Sie User Flows
   - Erstellen Sie Wireframes & Mockups

2. **Design System**
   - Material Design 3 für Android
   - Konsistente Farbpalette
   - Typography & Spacing

## 📋 Nächste Schritte

### Phase 1: Setup & Planning (Aktuell - Woche 1-2)
- [x] Repository-Struktur erstellt
- [x] Dokumentation erstellt
- [x] Issue Templates konfiguriert
- [x] CI/CD Pipeline Basis erstellt
- [ ] Team zusammenstellen
- [ ] Milestones in GitHub anlegen
- [ ] Einzelissues für MVP erstellen
- [ ] Sprint Planning (erste 2 Sprints)

### Phase 2: MVP Development (Woche 3-10)
- [ ] Android App Grundgerüst
- [ ] Backend API Grundfunktionen
- [ ] Authentifizierung
- [ ] Einkommens-Tracking
- [ ] Lokale Datenpersistenz
- [ ] Basis-Synchronisierung
- [ ] Regel-basierte Empfehlungen
- [ ] Basis-Tests

### Phase 3: V1.0 Development (Woche 11-18)
- [ ] UI/UX Verbesserungen
- [ ] ML-Empfehlungen
- [ ] Push-Benachrichtigungen
- [ ] Erweiterte Synchronisierung
- [ ] Analytics Integration
- [ ] DSGVO-Compliance
- [ ] Umfassende Tests
- [ ] Produktions-Deployment

## 🎯 Modul-Übersicht

| Modul | Issue Template | Priorität | Status |
|-------|---------------|-----------|--------|
| 1. UX & Product Design | [01-ux-design.md](.github/ISSUE_TEMPLATE/01-ux-design.md) | High | 📋 Planning |
| 2. Android Development | [02-android-dev.md](.github/ISSUE_TEMPLATE/02-android-dev.md) | High | 📋 Planning |
| 3. Backend API | [03-backend-api.md](.github/ISSUE_TEMPLATE/03-backend-api.md) | High | 📋 Planning |
| 4. Empfehlungssystem | [04-recommendation-system.md](.github/ISSUE_TEMPLATE/04-recommendation-system.md) | Medium | 📋 Planning |
| 5. Persistenz & Sync | [05-persistence-sync.md](.github/ISSUE_TEMPLATE/05-persistence-sync.md) | High | 📋 Planning |
| 6. Benachrichtigungen | [06-notifications.md](.github/ISSUE_TEMPLATE/06-notifications.md) | Medium | 📋 Planning |
| 7. CI/CD & Deployment | [07-cicd-deployment.md](.github/ISSUE_TEMPLATE/07-cicd-deployment.md) | Medium | ✅ In Progress |
| 8. Tests & Monitoring | [08-testing-monitoring.md](.github/ISSUE_TEMPLATE/08-testing-monitoring.md) | High | 📋 Planning |
| 9. Datenschutz & Security | [09-privacy-security.md](.github/ISSUE_TEMPLATE/09-privacy-security.md) | High | 📋 Planning |

## 💼 Rollen & Verantwortlichkeiten

### Android Developer
- Jetpack Compose UI
- ViewModels & State Management
- Room Database
- API Integration
- **Siehe:** [android/README.md](android/README.md)

### Backend Developer
- FastAPI/Express/Ktor (TBD)
- PostgreSQL Datenbank
- REST API Endpoints
- Authentifizierung
- **Siehe:** [backend/README.md](backend/README.md)

### UX/UI Designer
- User Research
- Wireframes & Mockups
- Design System
- Usability Testing
- **Template:** [01-ux-design.md](.github/ISSUE_TEMPLATE/01-ux-design.md)

### DevOps Engineer
- CI/CD Pipeline
- Docker Setup
- Cloud Deployment
- Monitoring
- **Template:** [07-cicd-deployment.md](.github/ISSUE_TEMPLATE/07-cicd-deployment.md)

### QA Engineer
- Test Strategy
- Automated Tests
- Manual Testing
- Bug Tracking
- **Template:** [08-testing-monitoring.md](.github/ISSUE_TEMPLATE/08-testing-monitoring.md)

## 🔧 Entwicklungsumgebung

### Android
```bash
# Voraussetzungen
- Android Studio Arctic Fox+
- JDK 17+
- Android SDK 24+ (Min), 34+ (Target)

# Setup
cd android
# Android Studio öffnen und Projekt importieren
```

### Backend (Python/FastAPI)
```bash
# Voraussetzungen
- Python 3.11+
- PostgreSQL 14+
- Docker (optional)

# Setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # Wenn vorhanden
```

### Backend (Node.js/Express)
```bash
# Voraussetzungen
- Node.js 18+
- PostgreSQL 14+
- Docker (optional)

# Setup
cd backend
npm install  # Wenn package.json vorhanden
```

## 📚 Wichtige Links

### Dokumentation
- [Project Overview](PROJECT.md)
- [Architecture](docs/architecture/README.md)
- [API Docs](docs/api/README.md)
- [Deployment](docs/DEPLOYMENT.md)

### GitHub
- [Issues](https://github.com/loopwaveeeeee/sabsteckapi/issues)
- [Projects](https://github.com/loopwaveeeeee/sabsteckapi/projects)
- [Milestones](https://github.com/loopwaveeeeee/sabsteckapi/milestones)
- [Pull Requests](https://github.com/loopwaveeeeee/sabsteckapi/pulls)

### Externe Ressourcen
- [Kotlin Docs](https://kotlinlang.org/docs/home.html)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)

## ❓ Häufige Fragen

### Wie erstelle ich ein neues Issue?
1. Gehe zu [Issues](https://github.com/loopwaveeeeee/sabsteckapi/issues)
2. Klicke "New Issue"
3. Wähle das passende Template
4. Fülle alle relevanten Felder aus
5. Weise Labels und Milestone zu

### Wie trage ich Code bei?
1. Fork das Repository
2. Erstelle einen Feature Branch
3. Implementiere deine Änderungen
4. Schreibe Tests
5. Erstelle einen Pull Request
6. Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details

### Welches Backend-Framework verwenden wir?
Noch nicht entschieden. Optionen:
- FastAPI (Python)
- Express.js (Node.js)
- Ktor (Kotlin)

Die Entscheidung wird im Team getroffen.

### Wann ist das MVP fertig?
Geplant: 6-8 Wochen nach Start der Entwicklung

### Wie kann ich helfen?
1. Lies die Dokumentation
2. Schau dir offene Issues an
3. Issues mit "good first issue" Label sind für Einsteiger
4. Frage im Team nach, wo Hilfe benötigt wird

## 🎉 Los geht's!

Bereit anzufangen? Wählen Sie einen Bereich:

1. **[Erstelle dein erstes Issue](https://github.com/loopwaveeeeee/sabsteckapi/issues/new/choose)**
2. **[Lies die Contributing Guidelines](CONTRIBUTING.md)**
3. **[Erkunde die Architektur](docs/architecture/README.md)**
4. **[Setup deine Entwicklungsumgebung](android/README.md)** oder **[Backend](backend/README.md)**

Viel Erfolg! 🚀
