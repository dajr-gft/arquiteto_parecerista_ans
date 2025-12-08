"""
Vertex AI Evaluation Service module for BV ANS Agent.
"""

from .dataset import EVALUATION_DATASET, get_dataset_stats
from .vertex_ai_evaluation import VertexAIEvaluationService, VertexAIEvaluationConfig

__all__ = [
    "EVALUATION_DATASET",
    "get_dataset_stats",
    "VertexAIEvaluationService",
    "VertexAIEvaluationConfig"
]

