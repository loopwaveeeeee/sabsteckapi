# Deployment Guide

Dieses Dokument beschreibt den Deployment-Prozess für das automatisierte Einkommens-Setup-Projekt.

## Übersicht

### Environments

1. **Development** - Lokale Entwicklung
2. **Staging** - Test-Umgebung
3. **Production** - Live-System

## Backend Deployment

### Docker Deployment (empfohlen)

#### 1. Build Docker Image

```bash
cd backend
docker build -t sabsteckapi-backend:latest .
```

#### 2. Run with Docker Compose

```bash
docker-compose up -d
```

**docker-compose.yml Beispiel:**
```yaml
version: '3.8'

services:
  backend:
    image: sabsteckapi-backend:latest
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/sabsteckapi
      - SECRET_KEY=${SECRET_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:14
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=sabsteckapi
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

### Cloud Deployment Optionen

#### Option 1: Railway

1. Erstelle Railway-Account
2. Verbinde GitHub Repository
3. Konfiguriere Environment Variables
4. Deploy mit einem Klick

```bash
# Railway CLI
railway login
railway init
railway up
```

#### Option 2: Render

1. Erstelle Render-Account
2. Verbinde GitHub Repository
3. Wähle "Web Service"
4. Konfiguriere Build & Start Commands

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn src.main:app --host 0.0.0.0 --port $PORT
```

#### Option 3: AWS (EC2 + RDS)

1. EC2 Instance erstellen
2. RDS PostgreSQL Datenbank erstellen
3. ElastiCache Redis (optional)
4. Security Groups konfigurieren
5. Docker installieren & deployen

```bash
# EC2 Setup
ssh ubuntu@your-ec2-ip
sudo apt update
sudo apt install docker.io docker-compose
git clone https://github.com/loopwaveeeeee/sabsteckapi.git
cd sabsteckapi/backend
docker-compose up -d
```

#### Option 4: Google Cloud Platform (Cloud Run)

```bash
# Build & Push
gcloud builds submit --tag gcr.io/PROJECT_ID/sabsteckapi-backend

# Deploy
gcloud run deploy sabsteckapi-backend \
  --image gcr.io/PROJECT_ID/sabsteckapi-backend \
  --platform managed \
  --region europe-west1 \
  --allow-unauthenticated
```

### Environment Variables

Erstellen Sie `.env` für Production:

```env
# Database
DATABASE_URL=postgresql://user:password@host:5432/sabsteckapi

# JWT
SECRET_KEY=your-super-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
ALLOWED_ORIGINS=https://app.sabsteck.com,https://www.sabsteck.com

# Redis
REDIS_URL=redis://redis-host:6379

# Environment
ENVIRONMENT=production
DEBUG=false

# Logging
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Database Migration

```bash
# Alembic (Python)
alembic upgrade head

# Prisma (Node.js)
npx prisma migrate deploy
```

### SSL/TLS

Verwenden Sie Let's Encrypt für kostenloses SSL:

```bash
# Mit Certbot
sudo certbot --nginx -d api.sabsteck.com
```

Oder nutzen Sie Cloud-Provider SSL (automatisch bei Railway, Render, etc.)

## Android App Deployment

### Build Release APK/AAB

```bash
cd android
./gradlew assembleRelease  # APK
./gradlew bundleRelease     # AAB (empfohlen für Play Store)
```

### Signing Configuration

**app/build.gradle.kts:**
```kotlin
android {
    signingConfigs {
        create("release") {
            storeFile = file(System.getenv("KEYSTORE_FILE") ?: "keystore.jks")
            storePassword = System.getenv("KEYSTORE_PASSWORD")
            keyAlias = System.getenv("KEY_ALIAS")
            keyPassword = System.getenv("KEY_PASSWORD")
        }
    }
    
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")
            isMinifyEnabled = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
```

### Google Play Store

1. **Erstelle Developer Account** (25€ einmalig)
2. **Erstelle App** in Play Console
3. **Upload AAB** (Android App Bundle)
4. **Fülle Store Listing aus**
   - App-Name
   - Beschreibung
   - Screenshots
   - Icon
5. **Content Rating**
6. **Privacy Policy**
7. **Pricing & Distribution**
8. **Submit for Review**

### Beta Testing (Google Play)

1. Erstelle **Closed/Open Testing Track**
2. Upload AAB
3. Teile Test-Link mit Beta-Testern

## CI/CD Setup

### GitHub Actions (bereits konfiguriert)

Workflow wird automatisch ausgeführt bei:
- Push auf `main` oder `develop`
- Pull Requests

**Erweiterte Deployment:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
        run: |
          npm install -g @railway/cli
          railway up
```

### Secrets Configuration

In GitHub Repository Settings > Secrets:

- `RAILWAY_TOKEN` - Railway API Token
- `KEYSTORE_FILE` - Android Keystore (Base64)
- `KEYSTORE_PASSWORD` - Keystore Password
- `KEY_ALIAS` - Key Alias
- `KEY_PASSWORD` - Key Password
- `GOOGLE_SERVICES_JSON` - Firebase Config (Base64)

## Monitoring & Logging

### Backend Monitoring

**Option 1: Sentry (Error Tracking)**
```bash
pip install sentry-sdk
```

**src/main.py:**
```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    environment="production"
)
```

**Option 2: Datadog**
```bash
pip install ddtrace
```

**Option 3: New Relic**
```bash
pip install newrelic
```

### Android Monitoring

**Firebase Crashlytics:**

**app/build.gradle.kts:**
```kotlin
plugins {
    id("com.google.gms.google-services")
    id("com.google.firebase.crashlytics")
}

dependencies {
    implementation("com.google.firebase:firebase-crashlytics-ktx")
    implementation("com.google.firebase:firebase-analytics-ktx")
}
```

## Backup Strategy

### Database Backup

**Automated PostgreSQL Backup:**
```bash
# Cron job (täglich)
0 2 * * * pg_dump -U user sabsteckapi > /backups/sabsteckapi_$(date +\%Y\%m\%d).sql
```

**Backup zu S3:**
```bash
# Mit AWS CLI
aws s3 cp /backups/sabsteckapi_20251023.sql s3://your-bucket/backups/
```

### Restore Database

```bash
psql -U user sabsteckapi < backup.sql
```

## Rollback Strategy

### Backend Rollback

**Docker:**
```bash
# Previous version
docker-compose down
docker run sabsteckapi-backend:v1.0.0
```

**Railway/Render:**
- Rollback über UI zu vorheriger Deployment

### Android Rollback

- Google Play erlaubt Rollback zu vorherigen Versionen
- Emergency Rollout für kritische Bugs

## Health Checks

### Backend Health Endpoint

```python
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": await check_db_connection()
    }
```

### Monitoring Health

```bash
# Uptime monitoring (z.B. UptimeRobot)
curl https://api.sabsteck.com/health
```

## Performance Optimization

### Backend
- Enable Gzip compression
- Configure connection pooling
- Redis caching
- CDN for static assets

### Android
- Enable R8/ProGuard
- Optimize images
- Lazy loading
- Background task optimization

## Security Checklist

- [ ] HTTPS/TLS aktiviert
- [ ] Secrets als Environment Variables
- [ ] Database Firewall konfiguriert
- [ ] API Rate Limiting aktiv
- [ ] Security Headers gesetzt
- [ ] Input Validation
- [ ] SQL Injection Prevention
- [ ] CORS korrekt konfiguriert
- [ ] Android App Obfuscation
- [ ] Regular Security Updates

## Post-Deployment

1. **Smoke Tests** durchführen
2. **Monitoring** prüfen
3. **Error Rates** überwachen
4. **Performance Metrics** checken
5. **User Feedback** sammeln

## Support & Maintenance

- **Monitoring:** 24/7 Error Tracking
- **Updates:** Regelmäßige Security Patches
- **Backups:** Tägliche automatische Backups
- **Documentation:** Aktuell halten

## Weitere Ressourcen

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com)
- [Google Play Console](https://play.google.com/console)
- [Railway Docs](https://docs.railway.app)
