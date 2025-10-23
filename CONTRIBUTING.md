# Beitragsrichtlinien

Vielen Dank für Ihr Interesse, zu diesem Projekt beizutragen!

## 🌟 Wie kann ich beitragen?

### Issues melden
1. Prüfen Sie, ob das Issue bereits existiert
2. Verwenden Sie die entsprechende Issue-Vorlage
3. Geben Sie eine klare Beschreibung an
4. Fügen Sie Screenshots/Logs hinzu, falls relevant

### Code beitragen

#### 1. Repository forken und klonen
```bash
git clone https://github.com/IHR-USERNAME/sabsteckapi.git
cd sabsteckapi
```

#### 2. Branch erstellen
```bash
git checkout -b feature/ihre-feature-beschreibung
# oder
git checkout -b fix/ihr-bugfix-beschreibung
```

#### 3. Änderungen vornehmen
- Folgen Sie den Code-Style-Richtlinien
- Schreiben Sie Tests für neue Features
- Aktualisieren Sie die Dokumentation

#### 4. Testen
```bash
# Android Tests
cd android
./gradlew test

# Backend Tests (Beispiel für Python)
cd backend
pytest

# Backend Tests (Beispiel für Node.js)
cd backend
npm test
```

#### 5. Commit & Push
```bash
git add .
git commit -m "feat: Ihre Beschreibung"
git push origin feature/ihre-feature-beschreibung
```

#### 6. Pull Request erstellen
- Verwenden Sie eine klare Beschreibung
- Verlinken Sie relevante Issues
- Warten Sie auf Code Review

## 📝 Commit-Konventionen

Wir verwenden [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: Neue Funktion hinzufügen
fix: Bug beheben
docs: Dokumentation aktualisieren
style: Code-Formatierung (keine funktionalen Änderungen)
refactor: Code-Refactoring
test: Tests hinzufügen oder korrigieren
chore: Build-Prozess oder Hilfswerkzeuge aktualisieren
perf: Performance-Verbesserung
ci: CI/CD-Konfiguration ändern
```

Beispiele:
```bash
git commit -m "feat: Einkommens-Tracking-Feature hinzufügen"
git commit -m "fix: Synchronisierungsfehler bei Offline-Modus"
git commit -m "docs: API-Endpunkte dokumentieren"
```

## 🎨 Code-Style

### Kotlin (Android)
- Folgen Sie den [Kotlin Coding Conventions](https://kotlinlang.org/docs/coding-conventions.html)
- Verwenden Sie ktlint für Formatierung
- 4 Leerzeichen für Einrückung

### Python (Backend)
- Folgen Sie [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Verwenden Sie black für Formatierung
- Type hints verwenden
- 4 Leerzeichen für Einrückung

### JavaScript/TypeScript (Backend)
- Folgen Sie dem [Airbnb Style Guide](https://github.com/airbnb/javascript)
- Verwenden Sie ESLint & Prettier
- 2 Leerzeichen für Einrückung

## ✅ Pull Request Checkliste

Bevor Sie einen PR einreichen, stellen Sie sicher:

- [ ] Code folgt dem Projekt-Style
- [ ] Alle Tests bestehen
- [ ] Neue Tests wurden hinzugefügt (falls zutreffend)
- [ ] Dokumentation wurde aktualisiert
- [ ] Commit-Nachrichten folgen den Konventionen
- [ ] Branch ist auf dem neuesten Stand mit `main`
- [ ] Keine Merge-Konflikte vorhanden
- [ ] PR-Beschreibung ist klar und vollständig

## 🔍 Code Review Prozess

1. **Automatische Checks:** CI/CD-Pipeline muss erfolgreich sein
2. **Review:** Mindestens ein Maintainer muss den Code reviewen
3. **Änderungen:** Beheben Sie requested changes
4. **Merge:** Nach Freigabe wird der PR gemerged

## 🏗️ Entwicklungsumgebung

### Android
- Android Studio Arctic Fox oder neuer
- JDK 11+
- Android SDK 24+ (Minimum)
- Emulator oder physisches Gerät

### Backend (Python/FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Backend (Node.js/Express)
```bash
cd backend
npm install
npm run dev
```

## 🧪 Tests schreiben

### Android (JUnit + Mockito)
```kotlin
@Test
fun `test income calculation`() {
    val income = Income(amount = 1000.0)
    assertEquals(1000.0, income.amount)
}
```

### Backend (pytest)
```python
def test_create_income_endpoint():
    response = client.post("/api/income", json={"amount": 1000})
    assert response.status_code == 201
```

### Backend (Jest)
```javascript
describe('Income API', () => {
  test('should create income', async () => {
    const response = await request(app)
      .post('/api/income')
      .send({ amount: 1000 });
    expect(response.status).toBe(201);
  });
});
```

## 📦 Module & Verantwortlichkeiten

| Modul | Verantwortlichkeit |
|-------|-------------------|
| `android/` | Android App (UI, ViewModels, Repository) |
| `backend/` | Backend-API (Endpoints, Services, Database) |
| `docs/` | Dokumentation |
| `.github/` | CI/CD, Issue Templates |

## 🐛 Bug Reports

Verwenden Sie das Bug-Issue-Template und geben Sie an:
- Schritte zur Reproduktion
- Erwartetes Verhalten
- Tatsächliches Verhalten
- Screenshots/Logs
- Umgebung (Android-Version, Backend-Version, etc.)

## 💡 Feature Requests

Verwenden Sie das Feature-Issue-Template und beschreiben Sie:
- Use Case
- Vorgeschlagene Lösung
- Alternativen
- Priorität

## 📞 Kommunikation

- **Issues:** Für Bugs und Features
- **Discussions:** Für Fragen und Diskussionen
- **Pull Requests:** Für Code-Beiträge

## 🔒 Sicherheit

Wenn Sie eine Sicherheitslücke finden:
- **NICHT** als öffentliches Issue melden
- Kontaktieren Sie das Team direkt (TBD)
- Geben Sie Details zur Schwachstelle an

## 📜 Code of Conduct

Wir verpflichten uns zu einem respektvollen und inklusiven Umfeld. Bitte behandeln Sie alle Mitwirkenden mit Respekt.

## ❓ Fragen?

Haben Sie Fragen? Erstellen Sie eine Discussion oder kontaktieren Sie das Team.

Vielen Dank für Ihren Beitrag! 🎉
