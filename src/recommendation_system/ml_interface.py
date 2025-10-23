"""Interface for future ML model integration"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from .models import IncomeSetup, MLPrediction, Recommendation

logger = logging.getLogger(__name__)


class MLModelInterface(ABC):
    """
    Abstract interface for ML models.
    
    This interface allows for future integration of machine learning models
    without changing the core recommendation engine architecture.
    """

    def __init__(self, model_name: str, model_version: str):
        self.model_name = model_name
        self.model_version = model_version

    @abstractmethod
    def predict(self, setup: IncomeSetup) -> MLPrediction:
        """
        Make a prediction based on income setup.
        
        Args:
            setup: The income setup to analyze
            
        Returns:
            MLPrediction with model results
        """
        pass

    @abstractmethod
    def get_features(self, setup: IncomeSetup) -> Dict[str, float]:
        """
        Extract features from income setup for model input.
        
        Args:
            setup: The income setup to extract features from
            
        Returns:
            Dictionary of feature names to values
        """
        pass

    @abstractmethod
    def explain_prediction(self, prediction: MLPrediction) -> str:
        """
        Provide human-readable explanation of the prediction.
        
        Args:
            prediction: The prediction to explain
            
        Returns:
            Human-readable explanation string
        """
        pass


class MLRecommender(ABC):
    """
    Abstract interface for ML-based recommenders.
    
    This allows for future ML models that directly generate recommendations
    rather than just predictions.
    """

    def __init__(self, model_name: str, model_version: str):
        self.model_name = model_name
        self.model_version = model_version

    @abstractmethod
    def recommend(self, setup: IncomeSetup) -> List[Recommendation]:
        """
        Generate recommendations using ML model.
        
        Args:
            setup: The income setup to analyze
            
        Returns:
            List of ML-generated recommendations
        """
        pass

    @abstractmethod
    def train(self, training_data: List[Dict]) -> None:
        """
        Train or update the model with new data.
        
        Args:
            training_data: Training data for the model
        """
        pass


class DummyMLModel(MLModelInterface):
    """
    Dummy ML model for testing and demonstration purposes.
    
    This can be used as a template for implementing real ML models.
    """

    def __init__(self):
        super().__init__(model_name="dummy_model", model_version="0.1.0")
        logger.info("DummyMLModel initialized (for testing only)")

    def predict(self, setup: IncomeSetup) -> MLPrediction:
        """Make a dummy prediction"""
        features = self.get_features(setup)
        
        # Dummy prediction: predict optimal savings rate
        predicted_savings_rate = 0.20
        
        return MLPrediction(
            model_name=self.model_name,
            model_version=self.model_version,
            prediction_type="optimal_savings_rate",
            predicted_value=predicted_savings_rate,
            confidence=0.75,
            features_used=features,
        )

    def get_features(self, setup: IncomeSetup) -> Dict[str, float]:
        """Extract features from income setup"""
        return {
            "total_income": setup.total_monthly_income,
            "num_income_sources": float(len(setup.income_sources)),
            "monthly_expenses": setup.monthly_expenses,
            "disposable_income": setup.disposable_income,
            "savings_rate": setup.disposable_income / setup.total_monthly_income if setup.total_monthly_income > 0 else 0,
        }

    def explain_prediction(self, prediction: MLPrediction) -> str:
        """Provide explanation of the prediction"""
        return (
            f"Model '{self.model_name}' (v{self.model_version}) predicts "
            f"{prediction.prediction_type}: {prediction.predicted_value:.2%} "
            f"with {prediction.confidence:.0%} confidence. "
            f"Based on {len(prediction.features_used)} features."
        )


class MLModelRegistry:
    """
    Registry for managing multiple ML models.
    
    This allows the recommendation engine to use multiple models
    and combine their predictions.
    """

    def __init__(self):
        self._models: Dict[str, MLModelInterface] = {}
        self._recommenders: Dict[str, MLRecommender] = {}
        logger.info("MLModelRegistry initialized")

    def register_model(self, model_id: str, model: MLModelInterface) -> None:
        """Register an ML model"""
        self._models[model_id] = model
        logger.info(f"Registered ML model: {model_id} ({model.model_name} v{model.model_version})")

    def register_recommender(self, recommender_id: str, recommender: MLRecommender) -> None:
        """Register an ML recommender"""
        self._recommenders[recommender_id] = recommender
        logger.info(
            f"Registered ML recommender: {recommender_id} "
            f"({recommender.model_name} v{recommender.model_version})"
        )

    def get_model(self, model_id: str) -> Optional[MLModelInterface]:
        """Get a registered model by ID"""
        return self._models.get(model_id)

    def get_recommender(self, recommender_id: str) -> Optional[MLRecommender]:
        """Get a registered recommender by ID"""
        return self._recommenders.get(recommender_id)

    def get_all_predictions(self, setup: IncomeSetup) -> List[MLPrediction]:
        """Get predictions from all registered models"""
        predictions = []
        for model_id, model in self._models.items():
            try:
                prediction = model.predict(setup)
                predictions.append(prediction)
                logger.debug(f"Model {model_id} prediction: {prediction.predicted_value}")
            except Exception as e:
                logger.error(f"Error getting prediction from model {model_id}: {str(e)}", exc_info=True)
        return predictions

    def get_all_recommendations(self, setup: IncomeSetup) -> List[Recommendation]:
        """Get recommendations from all registered ML recommenders"""
        recommendations = []
        for recommender_id, recommender in self._recommenders.items():
            try:
                recs = recommender.recommend(setup)
                recommendations.extend(recs)
                logger.info(f"ML recommender {recommender_id} generated {len(recs)} recommendations")
            except Exception as e:
                logger.error(
                    f"Error getting recommendations from {recommender_id}: {str(e)}", 
                    exc_info=True
                )
        return recommendations

    def list_models(self) -> List[Dict[str, str]]:
        """List all registered models"""
        return [
            {
                "model_id": model_id,
                "model_name": model.model_name,
                "model_version": model.model_version,
            }
            for model_id, model in self._models.items()
        ]

    def list_recommenders(self) -> List[Dict[str, str]]:
        """List all registered recommenders"""
        return [
            {
                "recommender_id": recommender_id,
                "model_name": recommender.model_name,
                "model_version": recommender.model_version,
            }
            for recommender_id, recommender in self._recommenders.items()
        ]
