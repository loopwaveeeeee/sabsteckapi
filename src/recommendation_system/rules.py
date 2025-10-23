"""Rule-based engine for income optimization recommendations"""

import logging
import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from .models import (
    IncomeSetup,
    IncomeType,
    Recommendation,
    RecommendationPriority,
)

logger = logging.getLogger(__name__)


class Rule(ABC):
    """Abstract base class for recommendation rules"""

    def __init__(self, rule_id: str, name: str, description: str):
        self.rule_id = rule_id
        self.name = name
        self.description = description

    @abstractmethod
    def evaluate(self, setup: IncomeSetup) -> Optional[Recommendation]:
        """
        Evaluate the rule against an income setup.
        
        Args:
            setup: The income setup to evaluate
            
        Returns:
            A Recommendation if the rule triggers, None otherwise
        """
        pass

    def _create_recommendation(
        self,
        setup: IncomeSetup,
        title: str,
        description: str,
        priority: RecommendationPriority,
        rationale: str,
        estimated_benefit: Optional[float] = None,
        applicable_types: Optional[List[IncomeType]] = None,
        confidence: float = 1.0,
    ) -> Recommendation:
        """Helper method to create a recommendation"""
        return Recommendation(
            recommendation_id=str(uuid.uuid4()),
            person_id=setup.person_id,
            title=title,
            description=description,
            priority=priority,
            estimated_monthly_benefit=estimated_benefit,
            applicable_income_types=applicable_types or [],
            rationale=rationale,
            rule_ids=[self.rule_id],
            confidence_score=confidence,
        )


class DiversificationRule(Rule):
    """Rule 1: Recommends diversifying income sources"""

    def __init__(self):
        super().__init__(
            rule_id="rule_001_diversification",
            name="Income Diversification",
            description="Recommends diversifying income sources to reduce risk",
        )

    def evaluate(self, setup: IncomeSetup) -> Optional[Recommendation]:
        """Evaluate if income sources should be diversified"""
        # Check if user has only one income source
        if len(setup.income_sources) == 1:
            primary_source = setup.income_sources[0]
            
            # If the single source is salary, recommend adding passive income
            if primary_source.income_type == IncomeType.SALARY:
                return self._create_recommendation(
                    setup=setup,
                    title="Diversifiziere deine Einkommensquellen",
                    description=(
                        "Du hast aktuell nur eine Einkommensquelle (Gehalt). "
                        "Erwäge zusätzliche Einkommensströme wie Investments oder Freelancing, "
                        "um finanzielle Stabilität zu erhöhen."
                    ),
                    priority=RecommendationPriority.MEDIUM,
                    rationale=(
                        f"Nur eine Einkommensquelle erkannt: {primary_source.income_type.value}. "
                        "Diversifizierung reduziert Abhängigkeit und Risiko."
                    ),
                    estimated_benefit=setup.total_monthly_income * 0.15,
                    applicable_types=[IncomeType.INVESTMENT, IncomeType.FREELANCE, IncomeType.PASSIVE],
                    confidence=0.85,
                )
        
        # Check if income is highly concentrated in one source
        if len(setup.income_sources) > 1:
            max_source = max(setup.income_sources, key=lambda s: s.monthly_amount)
            concentration = max_source.monthly_amount / setup.total_monthly_income
            
            if concentration > 0.8:  # More than 80% from one source
                return self._create_recommendation(
                    setup=setup,
                    title="Reduziere Einkommenskonzentration",
                    description=(
                        f"Über 80% deines Einkommens stammt aus einer Quelle ({max_source.income_type.value}). "
                        "Baue weitere Einkommensquellen auf, um Risiken zu minimieren."
                    ),
                    priority=RecommendationPriority.MEDIUM,
                    rationale=(
                        f"Einkommenskonzentration bei {concentration:.1%}. "
                        "Empfohlene Diversifizierung für bessere Risikostreuung."
                    ),
                    estimated_benefit=setup.total_monthly_income * 0.10,
                    confidence=0.75,
                )
        
        return None


class SavingsOptimizationRule(Rule):
    """Rule 2: Recommends optimizing savings based on income"""

    def __init__(self):
        super().__init__(
            rule_id="rule_002_savings",
            name="Savings Optimization",
            description="Recommends optimal savings strategies based on income and expenses",
        )

    def evaluate(self, setup: IncomeSetup) -> Optional[Recommendation]:
        """Evaluate savings optimization opportunities"""
        disposable = setup.disposable_income
        
        # Low or negative disposable income
        if disposable <= 0:
            return self._create_recommendation(
                setup=setup,
                title="Ausgaben optimieren - Kritisch",
                description=(
                    "Deine Ausgaben übersteigen dein Einkommen. "
                    "Prüfe dringend deine Ausgaben und suche nach Einsparmöglichkeiten."
                ),
                priority=RecommendationPriority.CRITICAL,
                rationale=f"Negatives verfügbares Einkommen: {disposable:.2f} EUR",
                estimated_benefit=abs(disposable),
                confidence=1.0,
            )
        
        # Low savings rate (less than 10% of income)
        savings_rate = disposable / setup.total_monthly_income if setup.total_monthly_income > 0 else 0
        
        if savings_rate < 0.10:
            potential_savings = setup.total_monthly_income * 0.20 - disposable
            return self._create_recommendation(
                setup=setup,
                title="Sparquote erhöhen",
                description=(
                    f"Deine aktuelle Sparquote liegt bei {savings_rate:.1%}. "
                    "Experten empfehlen mindestens 10-20% zu sparen. "
                    "Überprüfe deine Ausgaben und identifiziere Einsparpotenziale."
                ),
                priority=RecommendationPriority.HIGH,
                rationale=(
                    f"Sparquote von {savings_rate:.1%} liegt unter empfohlenen 10%. "
                    "Höhere Sparquote verbessert langfristige finanzielle Sicherheit."
                ),
                estimated_benefit=potential_savings,
                confidence=0.90,
            )
        
        # Good savings rate but no defined goal
        if savings_rate >= 0.20 and not setup.savings_goal:
            return self._create_recommendation(
                setup=setup,
                title="Sparziel definieren",
                description=(
                    f"Du sparst bereits {savings_rate:.1%} deines Einkommens - gut gemacht! "
                    "Definiere nun konkrete Sparziele (z.B. Notfallfonds, Altersvorsorge, Immobilie), "
                    "um deine Motivation zu erhöhen."
                ),
                priority=RecommendationPriority.LOW,
                rationale=f"Gute Sparquote ({savings_rate:.1%}), aber kein definiertes Ziel",
                confidence=0.70,
            )
        
        return None


class TaxOptimizationRule(Rule):
    """Rule 3: Recommends tax optimization strategies"""

    def __init__(self):
        super().__init__(
            rule_id="rule_003_tax_optimization",
            name="Tax Optimization",
            description="Recommends strategies to optimize tax burden",
        )

    def evaluate(self, setup: IncomeSetup) -> Optional[Recommendation]:
        """Evaluate tax optimization opportunities"""
        # Check for multiple income sources without clear tax optimization
        has_freelance = any(s.income_type == IncomeType.FREELANCE for s in setup.income_sources)
        has_investment = any(s.income_type == IncomeType.INVESTMENT for s in setup.income_sources)
        has_business = any(s.income_type == IncomeType.BUSINESS for s in setup.income_sources)
        
        # High income with potential for tax optimization
        if setup.total_monthly_income > 5000 and not has_investment:
            estimated_benefit = setup.total_monthly_income * 0.08  # Estimate 8% tax savings
            return self._create_recommendation(
                setup=setup,
                title="Steueroptimierung durch Investments prüfen",
                description=(
                    "Bei deinem Einkommensniveau könnten steueroptimierte Investments "
                    "(z.B. ETFs mit Teilfreistellung, Altersvorsorge) deine Steuerlast reduzieren. "
                    "Konsultiere einen Steuerberater für individuelle Optimierung."
                ),
                priority=RecommendationPriority.HIGH,
                rationale=(
                    f"Monatseinkommen von {setup.total_monthly_income:.2f} EUR ohne Investment-Einkommen. "
                    "Steueroptimierte Anlagen können Steuerlast signifikant senken."
                ),
                estimated_benefit=estimated_benefit,
                applicable_types=[IncomeType.INVESTMENT],
                confidence=0.80,
            )
        
        # Freelance income without business structure
        if has_freelance and not has_business and setup.total_monthly_income > 3000:
            freelance_income = sum(
                s.monthly_amount for s in setup.income_sources 
                if s.income_type == IncomeType.FREELANCE
            )
            if freelance_income > 1500:  # Significant freelance income
                return self._create_recommendation(
                    setup=setup,
                    title="Gewerbeanmeldung prüfen",
                    description=(
                        f"Du erzielst {freelance_income:.2f} EUR aus Freelancing. "
                        "Eine Gewerbeanmeldung oder Kleinunternehmerregelung könnte steuerlich vorteilhaft sein. "
                        "Prüfe auch Vorsteuerabzugsmöglichkeiten."
                    ),
                    priority=RecommendationPriority.MEDIUM,
                    rationale=(
                        f"Signifikantes Freelance-Einkommen ({freelance_income:.2f} EUR) "
                        "könnte von formaler Geschäftsstruktur profitieren."
                    ),
                    estimated_benefit=freelance_income * 0.10,
                    applicable_types=[IncomeType.BUSINESS],
                    confidence=0.75,
                )
        
        return None


class RuleEngine:
    """Main rule engine that coordinates all rules"""

    def __init__(self):
        self.rules: List[Rule] = [
            DiversificationRule(),
            SavingsOptimizationRule(),
            TaxOptimizationRule(),
        ]
        logger.info(f"RuleEngine initialized with {len(self.rules)} rules")

    def add_rule(self, rule: Rule) -> None:
        """Add a new rule to the engine"""
        self.rules.append(rule)
        logger.info(f"Added rule: {rule.name} (ID: {rule.rule_id})")

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule from the engine"""
        initial_count = len(self.rules)
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        removed = len(self.rules) < initial_count
        if removed:
            logger.info(f"Removed rule with ID: {rule_id}")
        return removed

    def evaluate_all(self, setup: IncomeSetup) -> List[Recommendation]:
        """
        Evaluate all rules against an income setup.
        
        Args:
            setup: The income setup to evaluate
            
        Returns:
            List of recommendations from all triggered rules
        """
        recommendations = []
        
        logger.info(f"Evaluating {len(self.rules)} rules for person {setup.person_id}")
        
        for rule in self.rules:
            try:
                recommendation = rule.evaluate(setup)
                if recommendation:
                    recommendations.append(recommendation)
                    logger.info(
                        f"Rule '{rule.name}' triggered for person {setup.person_id}: {recommendation.title}"
                    )
            except Exception as e:
                logger.error(f"Error evaluating rule {rule.rule_id}: {str(e)}", exc_info=True)
        
        logger.info(f"Generated {len(recommendations)} recommendations for person {setup.person_id}")
        return recommendations

    def get_rules_info(self) -> List[dict]:
        """Get information about all registered rules"""
        return [
            {
                "rule_id": rule.rule_id,
                "name": rule.name,
                "description": rule.description,
            }
            for rule in self.rules
        ]
