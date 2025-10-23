"""Main recommendation engine that combines rule-based and ML approaches"""

import logging
from typing import List, Optional

import structlog

from .ml_interface import MLModelRegistry
from .models import IncomeSetup, Recommendation
from .rules import RuleEngine

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
)

logger = structlog.get_logger(__name__)


class RecommendationEngine:
    """
    Main recommendation engine that combines rule-based and ML approaches.
    
    This engine:
    - Evaluates rule-based recommendations
    - Integrates ML-based recommendations (when available)
    - Logs all recommendations for traceability
    - Provides a unified interface for getting optimized income setup recommendations
    """

    def __init__(
        self,
        rule_engine: Optional[RuleEngine] = None,
        ml_registry: Optional[MLModelRegistry] = None,
        enable_ml: bool = True,
    ):
        """
        Initialize the recommendation engine.
        
        Args:
            rule_engine: Rule engine instance (creates default if None)
            ml_registry: ML model registry (creates default if None)
            enable_ml: Whether to enable ML-based recommendations
        """
        self.rule_engine = rule_engine or RuleEngine()
        self.ml_registry = ml_registry or MLModelRegistry()
        self.enable_ml = enable_ml
        
        logger.info(
            "RecommendationEngine initialized",
            num_rules=len(self.rule_engine.rules),
            ml_enabled=self.enable_ml,
        )

    def get_recommendations(
        self,
        setup: IncomeSetup,
        include_ml: Optional[bool] = None,
    ) -> List[Recommendation]:
        """
        Get all recommendations for an income setup.
        
        Args:
            setup: The income setup to analyze
            include_ml: Override to enable/disable ML recommendations for this call
            
        Returns:
            List of all recommendations (rule-based and ML-based)
        """
        use_ml = include_ml if include_ml is not None else self.enable_ml
        
        logger.info(
            "Getting recommendations",
            person_id=setup.person_id,
            total_income=setup.total_monthly_income,
            num_sources=len(setup.income_sources),
            use_ml=use_ml,
        )
        
        recommendations = []
        
        # Get rule-based recommendations
        try:
            rule_recommendations = self.rule_engine.evaluate_all(setup)
            recommendations.extend(rule_recommendations)
            
            logger.info(
                "Rule-based recommendations generated",
                person_id=setup.person_id,
                count=len(rule_recommendations),
            )
            
            # Log each recommendation for traceability
            for rec in rule_recommendations:
                logger.info(
                    "Recommendation generated",
                    recommendation_id=rec.recommendation_id,
                    person_id=rec.person_id,
                    title=rec.title,
                    priority=rec.priority.value,
                    confidence=rec.confidence_score,
                    rule_ids=rec.rule_ids,
                    estimated_benefit=rec.estimated_monthly_benefit,
                )
        except Exception as e:
            logger.error(
                "Error generating rule-based recommendations",
                person_id=setup.person_id,
                error=str(e),
                exc_info=True,
            )
        
        # Get ML-based recommendations if enabled
        if use_ml:
            try:
                ml_recommendations = self.ml_registry.get_all_recommendations(setup)
                recommendations.extend(ml_recommendations)
                
                logger.info(
                    "ML-based recommendations generated",
                    person_id=setup.person_id,
                    count=len(ml_recommendations),
                )
                
                # Log ML predictions for analysis
                ml_predictions = self.ml_registry.get_all_predictions(setup)
                for prediction in ml_predictions:
                    logger.info(
                        "ML prediction made",
                        person_id=setup.person_id,
                        model_name=prediction.model_name,
                        prediction_type=prediction.prediction_type,
                        predicted_value=prediction.predicted_value,
                        confidence=prediction.confidence,
                    )
            except Exception as e:
                logger.error(
                    "Error generating ML-based recommendations",
                    person_id=setup.person_id,
                    error=str(e),
                    exc_info=True,
                )
        
        # Sort by priority (critical > high > medium > low)
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda r: priority_order.get(r.priority.value, 99))
        
        logger.info(
            "Recommendations completed",
            person_id=setup.person_id,
            total_recommendations=len(recommendations),
        )
        
        return recommendations

    def get_recommendations_summary(self, setup: IncomeSetup) -> dict:
        """
        Get a summary of recommendations with aggregated statistics.
        
        Args:
            setup: The income setup to analyze
            
        Returns:
            Dictionary with recommendations and summary statistics
        """
        recommendations = self.get_recommendations(setup)
        
        total_estimated_benefit = sum(
            rec.estimated_monthly_benefit or 0 for rec in recommendations
        )
        
        by_priority = {}
        for rec in recommendations:
            priority = rec.priority.value
            by_priority[priority] = by_priority.get(priority, 0) + 1
        
        summary = {
            "person_id": setup.person_id,
            "total_recommendations": len(recommendations),
            "total_estimated_monthly_benefit": total_estimated_benefit,
            "recommendations_by_priority": by_priority,
            "current_income": {
                "total_monthly": setup.total_monthly_income,
                "disposable": setup.disposable_income,
                "num_sources": len(setup.income_sources),
            },
            "recommendations": [
                {
                    "id": rec.recommendation_id,
                    "title": rec.title,
                    "priority": rec.priority.value,
                    "estimated_benefit": rec.estimated_monthly_benefit,
                    "confidence": rec.confidence_score,
                }
                for rec in recommendations
            ],
        }
        
        logger.info(
            "Recommendations summary generated",
            person_id=setup.person_id,
            summary=summary,
        )
        
        return summary

    def get_system_info(self) -> dict:
        """Get information about the recommendation system configuration"""
        return {
            "rule_engine": {
                "enabled": True,
                "rules": self.rule_engine.get_rules_info(),
            },
            "ml_engine": {
                "enabled": self.enable_ml,
                "models": self.ml_registry.list_models(),
                "recommenders": self.ml_registry.list_recommenders(),
            },
        }
