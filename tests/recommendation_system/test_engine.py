"""Tests for recommendation engine"""

import pytest

from src.recommendation_system.engine import RecommendationEngine
from src.recommendation_system.models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
)
from src.recommendation_system.rules import RuleEngine
from src.recommendation_system.ml_interface import MLModelRegistry, DummyMLModel


class TestRecommendationEngine:
    """Test RecommendationEngine"""

    def test_engine_initialization(self):
        engine = RecommendationEngine()
        assert engine.rule_engine is not None
        assert engine.ml_registry is not None
        assert engine.enable_ml is True

    def test_engine_with_custom_components(self):
        rule_engine = RuleEngine()
        ml_registry = MLModelRegistry()
        
        engine = RecommendationEngine(
            rule_engine=rule_engine,
            ml_registry=ml_registry,
            enable_ml=False,
        )
        
        assert engine.rule_engine is rule_engine
        assert engine.ml_registry is ml_registry
        assert engine.enable_ml is False

    def test_get_recommendations(self):
        engine = RecommendationEngine()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2800.0,
        )
        
        recommendations = engine.get_recommendations(setup)
        assert len(recommendations) > 0
        assert all(hasattr(rec, "recommendation_id") for rec in recommendations)

    def test_recommendations_sorted_by_priority(self):
        engine = RecommendationEngine()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=2000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2500.0,  # Negative disposable - should trigger critical
        )
        
        recommendations = engine.get_recommendations(setup)
        
        # Check that critical/high priority recommendations come first
        if len(recommendations) > 1:
            priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
            for i in range(len(recommendations) - 1):
                current_priority = priority_order.get(recommendations[i].priority.value, 99)
                next_priority = priority_order.get(recommendations[i + 1].priority.value, 99)
                assert current_priority <= next_priority

    def test_get_recommendations_with_ml_disabled(self):
        engine = RecommendationEngine(enable_ml=False)
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        recommendations = engine.get_recommendations(setup)
        # Should still get rule-based recommendations
        assert len(recommendations) > 0

    def test_get_recommendations_summary(self):
        engine = RecommendationEngine()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2800.0,
        )
        
        summary = engine.get_recommendations_summary(setup)
        
        assert "person_id" in summary
        assert summary["person_id"] == "test_001"
        assert "total_recommendations" in summary
        assert "total_estimated_monthly_benefit" in summary
        assert "recommendations_by_priority" in summary
        assert "current_income" in summary
        assert "recommendations" in summary

    def test_get_system_info(self):
        engine = RecommendationEngine()
        info = engine.get_system_info()
        
        assert "rule_engine" in info
        assert "ml_engine" in info
        assert info["rule_engine"]["enabled"] is True
        assert "rules" in info["rule_engine"]

    def test_ml_integration(self):
        """Test that ML models can be integrated"""
        ml_registry = MLModelRegistry()
        dummy_model = DummyMLModel()
        ml_registry.register_model("dummy", dummy_model)
        
        engine = RecommendationEngine(ml_registry=ml_registry, enable_ml=True)
        
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        # Should not raise an error
        recommendations = engine.get_recommendations(setup)
        assert isinstance(recommendations, list)

    def test_multiple_scenarios(self):
        """Test engine with different income scenarios"""
        engine = RecommendationEngine()
        
        scenarios = [
            # Low income, high expenses
            IncomeSetup(
                person_id="scenario_1",
                income_sources=[
                    IncomeSource(income_type=IncomeType.SALARY, monthly_amount=2000.0)
                ],
                tax_class=TaxClass.CLASS_1,
                monthly_expenses=1900.0,
            ),
            # High income, single source
            IncomeSetup(
                person_id="scenario_2",
                income_sources=[
                    IncomeSource(income_type=IncomeType.SALARY, monthly_amount=7000.0)
                ],
                tax_class=TaxClass.CLASS_1,
                monthly_expenses=4000.0,
            ),
            # Diversified income
            IncomeSetup(
                person_id="scenario_3",
                income_sources=[
                    IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0),
                    IncomeSource(income_type=IncomeType.INVESTMENT, monthly_amount=800.0),
                    IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=500.0),
                ],
                tax_class=TaxClass.CLASS_1,
                monthly_expenses=3000.0,
            ),
        ]
        
        for setup in scenarios:
            recommendations = engine.get_recommendations(setup)
            # Each scenario should generate at least some recommendations
            assert isinstance(recommendations, list)
