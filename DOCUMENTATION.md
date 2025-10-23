# Empfehlungssystem (Recommendation System) - Dokumentation

## Überblick

Das Empfehlungssystem (Recommendation System) für optimale Einkommens-Setups ist ein flexibles und erweiterbares System, das auf einer regelbasierten Engine aufbaut und für zukünftige Machine Learning (ML) Erweiterungen vorbereitet ist.

## Hauptkomponenten

### 1. Datenmodelle (`models.py`)

#### IncomeSetup
Repräsentiert das komplette Einkommens-Setup einer Person:
- **person_id**: Eindeutige Identifikation
- **income_sources**: Liste von Einkommensquellen
- **tax_class**: Steuerklasse (1-6)
- **monthly_expenses**: Monatliche Ausgaben
- **savings_goal**: Optionales Sparziel

#### IncomeSource
Einzelne Einkommensquelle mit:
- **income_type**: Art (SALARY, FREELANCE, INVESTMENT, RENTAL, BUSINESS, PASSIVE)
- **monthly_amount**: Monatlicher Betrag
- **tax_rate**: Optionaler Steuersatz
- **is_primary**: Haupt-Einkommensquelle

#### Recommendation
Empfehlung mit:
- **title**: Titel der Empfehlung
- **description**: Beschreibung
- **priority**: Priorität (CRITICAL, HIGH, MEDIUM, LOW)
- **estimated_monthly_benefit**: Geschätzter monatlicher Vorteil
- **rationale**: Begründung der Empfehlung
- **rule_ids**: IDs der auslösenden Regeln
- **confidence_score**: Konfidenz-Score (0-1)

### 2. Regel-Engine (`rules.py`)

Die Regel-Engine bewertet Einkommens-Setups und generiert Empfehlungen basierend auf definierten Regeln.

#### Implementierte Regeln (min. 3)

##### 1. DiversificationRule (Diversifizierungs-Regel)
**Zweck**: Empfiehlt Diversifizierung von Einkommensquellen

**Trigger-Bedingungen**:
- Nur eine Einkommensquelle vorhanden
- Mehr als 80% des Einkommens aus einer Quelle

**Beispiel-Empfehlung**:
```
Titel: "Diversifiziere deine Einkommensquellen"
Priorität: MEDIUM
Rationale: "Nur eine Einkommensquelle erkannt: salary. Diversifizierung reduziert Abhängigkeit und Risiko."
```

##### 2. SavingsOptimizationRule (Spar-Optimierungs-Regel)
**Zweck**: Optimiert Sparverhalten basierend auf Einkommen und Ausgaben

**Trigger-Bedingungen**:
- Negatives verfügbares Einkommen → CRITICAL
- Sparquote unter 10% → HIGH
- Gute Sparquote (>20%) ohne Sparziel → LOW

**Beispiel-Empfehlung**:
```
Titel: "Sparquote erhöhen"
Priorität: HIGH
Rationale: "Sparquote von 6.7% liegt unter empfohlenen 10%. Höhere Sparquote verbessert langfristige finanzielle Sicherheit."
```

##### 3. TaxOptimizationRule (Steueroptimierungs-Regel)
**Zweck**: Identifiziert Möglichkeiten zur Steueroptimierung

**Trigger-Bedingungen**:
- Hohes Einkommen (>5000€) ohne Investment-Einkommen
- Signifikantes Freelance-Einkommen ohne Gewerbestruktur

**Beispiel-Empfehlung**:
```
Titel: "Steueroptimierung durch Investments prüfen"
Priorität: HIGH
Rationale: "Monatseinkommen von 6000.00 EUR ohne Investment-Einkommen. Steueroptimierte Anlagen können Steuerlast signifikant senken."
```

#### RuleEngine-Klasse

Hauptklasse zur Koordination aller Regeln:

```python
engine = RuleEngine()

# Evaluiere alle Regeln
recommendations = engine.evaluate_all(income_setup)

# Füge neue Regel hinzu
engine.add_rule(custom_rule)

# Entferne Regel
engine.remove_rule("rule_id")

# Zeige Regel-Informationen
rules_info = engine.get_rules_info()
```

### 3. ML-Interface (`ml_interface.py`)

Vorbereitung für zukünftige Machine Learning Integration.

#### Abstrakte Interfaces

##### MLModelInterface
Basis-Interface für ML-Modelle:
- `predict(setup)`: Macht Vorhersagen
- `get_features(setup)`: Extrahiert Features
- `explain_prediction(prediction)`: Erklärt Vorhersage

##### MLRecommender
Interface für ML-basierte Empfehlungen:
- `recommend(setup)`: Generiert Empfehlungen
- `train(training_data)`: Trainiert Modell

#### DummyMLModel
Beispiel-Implementation für Tests und Demonstrationszwecke.

#### MLModelRegistry
Verwaltet mehrere ML-Modelle:
```python
registry = MLModelRegistry()
registry.register_model("model_id", ml_model)
predictions = registry.get_all_predictions(setup)
```

### 4. Hauptmotor (`engine.py`)

Die `RecommendationEngine` kombiniert regelbasierte und ML-Ansätze.

```python
# Initialisierung
engine = RecommendationEngine(
    rule_engine=RuleEngine(),
    ml_registry=MLModelRegistry(),
    enable_ml=True
)

# Empfehlungen erhalten
recommendations = engine.get_recommendations(income_setup)

# Zusammenfassung erhalten
summary = engine.get_recommendations_summary(income_setup)

# System-Info
info = engine.get_system_info()
```

## Logging und Nachvollziehbarkeit

Das System verwendet **strukturiertes Logging** (structlog) für vollständige Nachvollziehbarkeit:

### Was wird geloggt?

1. **Initialisierung**
   ```json
   {
     "event": "RecommendationEngine initialized",
     "num_rules": 3,
     "ml_enabled": true,
     "timestamp": "2025-10-23T21:00:00Z"
   }
   ```

2. **Regel-Evaluierung**
   ```json
   {
     "event": "Rule triggered",
     "person_id": "person_001",
     "rule_name": "DiversificationRule",
     "timestamp": "2025-10-23T21:00:01Z"
   }
   ```

3. **Generierte Empfehlungen**
   ```json
   {
     "event": "Recommendation generated",
     "recommendation_id": "uuid-123",
     "person_id": "person_001",
     "title": "Diversifiziere deine Einkommensquellen",
     "priority": "medium",
     "confidence": 0.85,
     "rule_ids": ["rule_001_diversification"],
     "estimated_benefit": 525.0,
     "timestamp": "2025-10-23T21:00:01Z"
   }
   ```

4. **ML-Vorhersagen**
   ```json
   {
     "event": "ML prediction made",
     "person_id": "person_001",
     "model_name": "dummy_model",
     "prediction_type": "optimal_savings_rate",
     "predicted_value": 0.20,
     "confidence": 0.75,
     "timestamp": "2025-10-23T21:00:02Z"
   }
   ```

## Testszenarien

Das System enthält 8 vordefinierte Testszenarien in `test_scenarios.py`:

1. **single_salary**: Einzelne Gehaltsquelle
2. **high_earner_no_diversification**: Gutverdiener ohne Diversifizierung
3. **diversified_good_savings**: Gut diversifiziert mit guter Sparquote
4. **freelancer_concentrated**: Freelancer mit Einkommenskonzentration
5. **low_savings_critical**: Kritisch niedrige Sparquote
6. **negative_disposable**: Ausgaben übersteigen Einkommen
7. **high_concentration**: Hohe Konzentration trotz mehrerer Quellen
8. **optimal_setup**: Optimales Setup (minimale Empfehlungen)

## Verwendung

### Grundlegende Verwendung

```python
from src.recommendation_system import (
    RecommendationEngine,
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)

# Setup erstellen
setup = IncomeSetup(
    person_id="user_123",
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

# Engine initialisieren
engine = RecommendationEngine()

# Empfehlungen erhalten
recommendations = engine.get_recommendations(setup)

# Empfehlungen ausgeben
for rec in recommendations:
    print(f"[{rec.priority.value}] {rec.title}")
    print(f"  {rec.description}")
    print(f"  Estimated benefit: €{rec.estimated_monthly_benefit:.2f}")
```

### Demo-Script verwenden

```bash
# Alle Szenarien durchlaufen
python demo.py

# Spezifisches Szenario
python demo.py --scenario single_salary

# Verbose-Modus
python demo.py --verbose

# Interaktiver Modus
python demo.py --interactive
```

## Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=src/recommendation_system --cov-report=html

# Spezifische Tests
pytest tests/recommendation_system/test_rules.py
pytest tests/recommendation_system/test_engine.py
```

## Erweiterbarkeit

### Neue Regel hinzufügen

```python
from src.recommendation_system.rules import Rule

class MyCustomRule(Rule):
    def __init__(self):
        super().__init__(
            rule_id="rule_004_custom",
            name="Custom Rule",
            description="My custom rule description"
        )
    
    def evaluate(self, setup: IncomeSetup) -> Optional[Recommendation]:
        # Implementiere deine Logik
        if some_condition:
            return self._create_recommendation(
                setup=setup,
                title="Custom Recommendation",
                description="...",
                priority=RecommendationPriority.MEDIUM,
                rationale="...",
            )
        return None

# Regel zur Engine hinzufügen
engine.rule_engine.add_rule(MyCustomRule())
```

### ML-Modell integrieren

```python
from src.recommendation_system.ml_interface import MLModelInterface

class MyMLModel(MLModelInterface):
    def __init__(self):
        super().__init__(
            model_name="my_model",
            model_version="1.0.0"
        )
    
    def predict(self, setup: IncomeSetup) -> MLPrediction:
        # Implementiere Vorhersage-Logik
        features = self.get_features(setup)
        # ... ML-Logik ...
        return MLPrediction(...)
    
    def get_features(self, setup: IncomeSetup) -> Dict[str, float]:
        # Feature-Extraktion
        return {...}
    
    def explain_prediction(self, prediction: MLPrediction) -> str:
        # Erkläre Vorhersage
        return "..."

# Modell registrieren
engine.ml_registry.register_model("my_model", MyMLModel())
```

## Architektur-Diagramm

```
┌─────────────────────────────────────────────┐
│         RecommendationEngine                │
│  (Hauptkoordinator)                         │
└────────────┬──────────────┬─────────────────┘
             │              │
      ┌──────▼──────┐  ┌───▼────────────┐
      │ RuleEngine  │  │ MLModelRegistry│
      │             │  │                │
      └──────┬──────┘  └───┬────────────┘
             │              │
    ┌────────▼────────┐    │
    │ Rules:          │    │
    │ - Diversif.     │    │
    │ - Savings       │    │
    │ - Tax Optim.    │    │
    │ - Custom...     │    │
    └─────────────────┘    │
                      ┌────▼──────────┐
                      │ ML Models:    │
                      │ - Dummy       │
                      │ - Future ML   │
                      └───────────────┘
```

## Anforderungen erfüllt

✅ **Regelbasierte Engine implementiert** (min. 3 Regeln)
- DiversificationRule
- SavingsOptimizationRule
- TaxOptimizationRule

✅ **Schnittstelle für ML vorbereitet**
- MLModelInterface (abstraktes Interface)
- MLRecommender (abstraktes Interface)
- MLModelRegistry (Verwaltung)
- DummyMLModel (Beispiel-Implementation)

✅ **Testszenarien dokumentiert**
- 8 vordefinierte Szenarien
- Demo-Script mit interaktivem Modus
- Comprehensive Tests

✅ **Nachvollziehbarkeit (Logging der Empfehlungen)**
- Strukturiertes Logging (structlog)
- Alle Empfehlungen werden mit Details geloggt
- Regel-IDs, Konfidenz-Scores, und Rationale nachvollziehbar

## Zukünftige Erweiterungen

1. **ML-Modell-Integration**
   - Implementierung echter ML-Modelle (z.B. mit scikit-learn)
   - Training mit historischen Daten
   - A/B-Testing von Empfehlungen

2. **Erweiterte Regeln**
   - Altersvorsorge-Optimierung
   - Risikomanagement
   - Liquiditätsplanung

3. **API-Integration**
   - REST API für externe Systeme
   - Webhook-Support für Notifications
   - Batch-Processing für multiple Setups

4. **Visualisierung**
   - Dashboard für Empfehlungen
   - Vergleich verschiedener Szenarien
   - Tracking von implementierten Empfehlungen
