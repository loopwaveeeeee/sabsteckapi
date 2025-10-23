"""Tests for ML interface"""

import pytest

from src.recommendation_system.models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)
from src.recommendation_system.ml_interface import (
    DummyMLModel,
    MLModelRegistry,
)


class TestDummyMLModel:
    """Test DummyMLModel"""

    def test_model_initialization(self):
        model = DummyMLModel()
        assert model.model_name == "dummy_model"
        assert model.model_version == "0.1.0"

    def test_predict(self):
        model = DummyMLModel()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        prediction = model.predict(setup)
        assert prediction.model_name == "dummy_model"
        assert prediction.prediction_type == "optimal_savings_rate"
        assert 0 <= prediction.confidence <= 1

    def test_get_features(self):
        model = DummyMLModel()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0),
                IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=1000.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2500.0,
        )
        
        features = model.get_features(setup)
        assert features["total_income"] == 4000.0
        assert features["num_income_sources"] == 2.0
        assert features["monthly_expenses"] == 2500.0
        assert features["disposable_income"] == 1500.0

    def test_explain_prediction(self):
        model = DummyMLModel()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        prediction = model.predict(setup)
        explanation = model.explain_prediction(prediction)
        assert "dummy_model" in explanation
        assert "confidence" in explanation.lower()


class TestMLModelRegistry:
    """Test MLModelRegistry"""

    def test_registry_initialization(self):
        registry = MLModelRegistry()
        assert len(registry.list_models()) == 0
        assert len(registry.list_recommenders()) == 0

    def test_register_model(self):
        registry = MLModelRegistry()
        model = DummyMLModel()
        
        registry.register_model("dummy", model)
        assert len(registry.list_models()) == 1
        
        retrieved = registry.get_model("dummy")
        assert retrieved is model

    def test_get_all_predictions(self):
        registry = MLModelRegistry()
        model = DummyMLModel()
        registry.register_model("dummy", model)
        
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        predictions = registry.get_all_predictions(setup)
        assert len(predictions) == 1
        assert predictions[0].model_name == "dummy_model"

    def test_list_models(self):
        registry = MLModelRegistry()
        model1 = DummyMLModel()
        model2 = DummyMLModel()
        
        registry.register_model("model1", model1)
        registry.register_model("model2", model2)
        
        models = registry.list_models()
        assert len(models) == 2
        assert all("model_id" in m for m in models)
        assert all("model_name" in m for m in models)
