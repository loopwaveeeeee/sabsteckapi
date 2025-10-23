"""Data models for the recommendation system"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class IncomeType(str, Enum):
    """Types of income sources"""
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENT = "investment"
    RENTAL = "rental"
    BUSINESS = "business"
    PASSIVE = "passive"


class TaxClass(str, Enum):
    """German tax classes (Steuerklassen)"""
    CLASS_1 = "1"  # Single, no children
    CLASS_2 = "2"  # Single parent
    CLASS_3 = "3"  # Married, higher income
    CLASS_4 = "4"  # Married, equal income
    CLASS_5 = "5"  # Married, lower income
    CLASS_6 = "6"  # Second job


class IncomeSource(BaseModel):
    """Represents a single income source"""
    income_type: IncomeType
    monthly_amount: float = Field(gt=0, description="Monthly income in EUR")
    tax_rate: Optional[float] = Field(None, ge=0, le=1, description="Effective tax rate")
    is_primary: bool = Field(default=False, description="Whether this is primary income")
    description: Optional[str] = None


class IncomeSetup(BaseModel):
    """Represents a complete income setup for a person"""
    person_id: str
    income_sources: List[IncomeSource]
    tax_class: TaxClass
    monthly_expenses: float = Field(ge=0, description="Monthly expenses in EUR")
    savings_goal: Optional[float] = Field(None, ge=0, description="Monthly savings goal in EUR")
    metadata: Dict[str, str] = Field(default_factory=dict)

    @property
    def total_monthly_income(self) -> float:
        """Calculate total monthly income"""
        return sum(source.monthly_amount for source in self.income_sources)

    @property
    def disposable_income(self) -> float:
        """Calculate disposable income after expenses"""
        return self.total_monthly_income - self.monthly_expenses


class RecommendationPriority(str, Enum):
    """Priority levels for recommendations"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Recommendation(BaseModel):
    """Represents a recommendation for income optimization"""
    recommendation_id: str
    person_id: str
    title: str
    description: str
    priority: RecommendationPriority
    estimated_monthly_benefit: Optional[float] = Field(None, description="Estimated benefit in EUR")
    applicable_income_types: List[IncomeType] = Field(default_factory=list)
    rationale: str = Field(description="Explanation of why this recommendation was made")
    rule_ids: List[str] = Field(default_factory=list, description="IDs of rules that triggered this")
    confidence_score: float = Field(default=1.0, ge=0, le=1, description="Confidence in recommendation")
    created_at: datetime = Field(default_factory=datetime.now)
    metadata: Dict[str, str] = Field(default_factory=dict)


class MLPrediction(BaseModel):
    """Model for ML predictions (interface for future ML integration)"""
    model_name: str
    model_version: str
    prediction_type: str
    predicted_value: float
    confidence: float = Field(ge=0, le=1)
    features_used: Dict[str, float] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
