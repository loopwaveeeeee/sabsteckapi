# Sabsteck API - Empfehlungssystem

Ein intelligentes Empfehlungssystem für optimale Einkommens-Setups mit regelbasierter Engine und ML-Vorbereitung.

## Features

✨ **Regelbasierte Empfehlungen**
- Diversifizierung von Einkommensquellen
- Spar-Optimierung
- Steueroptimierung
- Flexibel erweiterbar

🤖 **ML-Integration vorbereitet**
- Abstrakte Interfaces für ML-Modelle
- Model Registry für Multiple-Modell-Verwaltung
- Beispiel-Implementation (DummyMLModel)

📊 **Testszenarien & Simulation**
- 8 vordefinierte Testszenarien
- Interaktiver Demo-Modus
- Umfassende Test-Suite

📝 **Logging & Nachvollziehbarkeit**
- Strukturiertes Logging (JSON)
- Vollständige Nachverfolgung aller Empfehlungen
- Konfidenz-Scores und Begründungen

## Quick Start

### Installation

```bash
# Dependencies installieren
pip install -r requirements.txt
```

### Demo ausführen

```bash
# Alle Testszenarien durchlaufen
python demo.py

# Spezifisches Szenario testen
python demo.py --scenario single_salary --verbose

# Interaktiver Modus
python demo.py --interactive
```

### Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage-Report
pytest --cov=src/recommendation_system --cov-report=html

# Spezifische Tests
pytest tests/recommendation_system/test_rules.py -v
```

## Verwendung

```python
from src.recommendation_system import (
    RecommendationEngine,
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)

# Income Setup erstellen
setup = IncomeSetup(
    person_id="user_001",
    income_sources=[
        IncomeSource(
            income_type=IncomeType.SALARY,
            monthly_amount=3500.0,
            is_primary=True,
        )
    ],
    tax_class=TaxClass.CLASS_1,
    monthly_expenses=2800.0,
)

# Recommendation Engine initialisieren
engine = RecommendationEngine()

# Empfehlungen erhalten
recommendations = engine.get_recommendations(setup)

for rec in recommendations:
    print(f"[{rec.priority.value}] {rec.title}")
    print(f"  → {rec.description}")
    if rec.estimated_monthly_benefit:
        print(f"  💰 Benefit: €{rec.estimated_monthly_benefit:.2f}/Monat")
```

## Struktur

```
sabsteckapi/
├── src/
│   └── recommendation_system/
│       ├── __init__.py           # Hauptexports
│       ├── models.py             # Datenmodelle
│       ├── rules.py              # Regelbasierte Engine
│       ├── ml_interface.py       # ML-Interfaces
│       ├── engine.py             # Hauptmotor
│       └── test_scenarios.py    # Testszenarien
├── tests/
│   └── recommendation_system/    # Umfassende Tests
├── demo.py                       # Demo-Script
├── requirements.txt              # Dependencies
├── DOCUMENTATION.md              # Ausführliche Dokumentation
└── README.md                     # Diese Datei
```

## Implementierte Regeln

1. **Diversifizierungs-Regel**: Empfiehlt Diversifizierung von Einkommensquellen bei hoher Konzentration
2. **Spar-Optimierungs-Regel**: Optimiert Sparverhalten basierend auf Einkommen und Ausgaben
3. **Steueroptimierungs-Regel**: Identifiziert Möglichkeiten zur Steueroptimierung

## ML-Erweiterbarkeit

Das System ist für zukünftige ML-Integration vorbereitet:

```python
from src.recommendation_system.ml_interface import MLModelInterface

class MyMLModel(MLModelInterface):
    def predict(self, setup):
        # ML-Logik hier
        pass
    
    def get_features(self, setup):
        # Feature-Extraktion
        pass

# Modell registrieren
engine.ml_registry.register_model("my_model", MyMLModel())
```

## Dokumentation

Siehe [DOCUMENTATION.md](DOCUMENTATION.md) für:
- Detaillierte Komponentenbeschreibung
- Logging-Format und Beispiele
- Erweiterungsanleitungen
- Architektur-Diagramme

## Anforderungen erfüllt

✅ Regel-Engine implementiert (min. 3 Regeln)  
✅ Schnittstelle für ML vorbereitet  
✅ Testszenarien dokumentiert  
✅ Nachvollziehbarkeit (Logging der Empfehlungen)

## Lizenz

Dieses Projekt ist Teil der Sabsteck API.

