"""Tests for data models"""

import pytest
from datetime import datetime

from src.recommendation_system.models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    Recommendation,
    RecommendationPriority,
    TaxClass,
    MLPrediction,
)


class TestIncomeSource:
    """Test IncomeSource model"""

    def test_create_income_source(self):
        source = IncomeSource(
            income_type=IncomeType.SALARY,
            monthly_amount=3000.0,
            is_primary=True,
        )
        assert source.income_type == IncomeType.SALARY
        assert source.monthly_amount == 3000.0
        assert source.is_primary is True

    def test_income_source_with_tax_rate(self):
        source = IncomeSource(
            income_type=IncomeType.FREELANCE,
            monthly_amount=2000.0,
            tax_rate=0.30,
        )
        assert source.tax_rate == 0.30


class TestIncomeSetup:
    """Test IncomeSetup model"""

    def test_create_income_setup(self):
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        assert setup.person_id == "test_001"
        assert len(setup.income_sources) == 1
        assert setup.tax_class == TaxClass.CLASS_1
        assert setup.monthly_expenses == 2000.0

    def test_total_monthly_income(self):
        setup = IncomeSetup(
            person_id="test_002",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0),
                IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=1000.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2500.0,
        )
        assert setup.total_monthly_income == 4000.0

    def test_disposable_income(self):
        setup = IncomeSetup(
            person_id="test_003",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        assert setup.disposable_income == 1000.0


class TestRecommendation:
    """Test Recommendation model"""

    def test_create_recommendation(self):
        rec = Recommendation(
            recommendation_id="rec_001",
            person_id="person_001",
            title="Test Recommendation",
            description="This is a test",
            priority=RecommendationPriority.HIGH,
            rationale="Testing purposes",
        )
        assert rec.recommendation_id == "rec_001"
        assert rec.priority == RecommendationPriority.HIGH
        assert rec.confidence_score == 1.0

    def test_recommendation_with_benefit(self):
        rec = Recommendation(
            recommendation_id="rec_002",
            person_id="person_002",
            title="Savings Optimization",
            description="Increase savings rate",
            priority=RecommendationPriority.MEDIUM,
            estimated_monthly_benefit=500.0,
            rationale="Current savings rate too low",
            confidence_score=0.85,
        )
        assert rec.estimated_monthly_benefit == 500.0
        assert rec.confidence_score == 0.85


class TestMLPrediction:
    """Test MLPrediction model"""

    def test_create_ml_prediction(self):
        prediction = MLPrediction(
            model_name="test_model",
            model_version="1.0.0",
            prediction_type="savings_rate",
            predicted_value=0.25,
            confidence=0.90,
        )
        assert prediction.model_name == "test_model"
        assert prediction.predicted_value == 0.25
        assert prediction.confidence == 0.90
