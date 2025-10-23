"""Tests for rule engine"""

import pytest

from src.recommendation_system.models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
    RecommendationPriority,
)
from src.recommendation_system.rules import (
    DiversificationRule,
    SavingsOptimizationRule,
    TaxOptimizationRule,
    RuleEngine,
)


class TestDiversificationRule:
    """Test DiversificationRule"""

    def test_single_salary_triggers_rule(self):
        rule = DiversificationRule()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2000.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert "Diversifiziere" in recommendation.title
        assert recommendation.priority == RecommendationPriority.MEDIUM

    def test_diversified_income_no_trigger(self):
        rule = DiversificationRule()
        setup = IncomeSetup(
            person_id="test_002",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=2000.0),
                IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=1500.0),
                IncomeSource(income_type=IncomeType.INVESTMENT, monthly_amount=1000.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=3000.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is None

    def test_high_concentration_triggers_rule(self):
        rule = DiversificationRule()
        setup = IncomeSetup(
            person_id="test_003",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=4500.0),
                IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=500.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=3000.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert "Konzentration" in recommendation.title or "konzentration" in recommendation.title.lower()


class TestSavingsOptimizationRule:
    """Test SavingsOptimizationRule"""

    def test_negative_disposable_income_critical(self):
        rule = SavingsOptimizationRule()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=2000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2500.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert recommendation.priority == RecommendationPriority.CRITICAL

    def test_low_savings_rate_high_priority(self):
        rule = SavingsOptimizationRule()
        setup = IncomeSetup(
            person_id="test_002",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2800.0,  # Only 200 savings = 6.7% rate
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert recommendation.priority == RecommendationPriority.HIGH

    def test_good_savings_no_goal_low_priority(self):
        rule = SavingsOptimizationRule()
        setup = IncomeSetup(
            person_id="test_003",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=4000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=3000.0,  # 25% savings rate
            savings_goal=None,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert recommendation.priority == RecommendationPriority.LOW
        assert "Ziel" in recommendation.title or "ziel" in recommendation.title.lower()


class TestTaxOptimizationRule:
    """Test TaxOptimizationRule"""

    def test_high_income_no_investment_triggers(self):
        rule = TaxOptimizationRule()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=6000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=3500.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert recommendation.priority == RecommendationPriority.HIGH
        assert "Steuer" in recommendation.title or "steuer" in recommendation.title.lower()

    def test_freelance_income_suggests_business_structure(self):
        rule = TaxOptimizationRule()
        setup = IncomeSetup(
            person_id="test_002",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=2000.0),
                IncomeSource(income_type=IncomeType.FREELANCE, monthly_amount=2000.0),
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2500.0,
        )
        
        recommendation = rule.evaluate(setup)
        assert recommendation is not None
        assert "Gewerbe" in recommendation.title or "gewerbe" in recommendation.title.lower()


class TestRuleEngine:
    """Test RuleEngine"""

    def test_rule_engine_initialization(self):
        engine = RuleEngine()
        assert len(engine.rules) >= 3  # At least 3 rules as required

    def test_evaluate_all_returns_recommendations(self):
        engine = RuleEngine()
        setup = IncomeSetup(
            person_id="test_001",
            income_sources=[
                IncomeSource(income_type=IncomeType.SALARY, monthly_amount=3000.0)
            ],
            tax_class=TaxClass.CLASS_1,
            monthly_expenses=2800.0,
        )
        
        recommendations = engine.evaluate_all(setup)
        assert len(recommendations) > 0

    def test_add_rule(self):
        engine = RuleEngine()
        initial_count = len(engine.rules)
        
        # Create a simple test rule
        class TestRule(DiversificationRule):
            def __init__(self):
                super().__init__()
                self.rule_id = "test_rule"
                self.name = "Test Rule"
        
        engine.add_rule(TestRule())
        assert len(engine.rules) == initial_count + 1

    def test_remove_rule(self):
        engine = RuleEngine()
        initial_count = len(engine.rules)
        
        # Remove first rule
        first_rule_id = engine.rules[0].rule_id
        result = engine.remove_rule(first_rule_id)
        
        assert result is True
        assert len(engine.rules) == initial_count - 1

    def test_get_rules_info(self):
        engine = RuleEngine()
        rules_info = engine.get_rules_info()
        
        assert len(rules_info) >= 3
        assert all("rule_id" in info for info in rules_info)
        assert all("name" in info for info in rules_info)
        assert all("description" in info for info in rules_info)
