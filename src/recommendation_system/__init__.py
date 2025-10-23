"""Recommendation System for optimal income setups"""

from .engine import RecommendationEngine
from .models import IncomeSetup, Recommendation
from .rules import RuleEngine

__all__ = ["RecommendationEngine", "IncomeSetup", "Recommendation", "RuleEngine"]
