"""Recommendation System for optimal income setups"""

from .engine import RecommendationEngine
from .models import (
    IncomeSetup,
    IncomeSource,
    IncomeType,
    TaxClass,
    Recommendation,
    RecommendationPriority,
    MLPrediction,
)
from .rules import RuleEngine
from .ml_interface import MLModelRegistry, MLModelInterface, MLRecommender

__all__ = [
    "RecommendationEngine",
    "IncomeSetup",
    "IncomeSource",
    "IncomeType",
    "TaxClass",
    "Recommendation",
    "RecommendationPriority",
    "MLPrediction",
    "RuleEngine",
    "MLModelRegistry",
    "MLModelInterface",
    "MLRecommender",
]
