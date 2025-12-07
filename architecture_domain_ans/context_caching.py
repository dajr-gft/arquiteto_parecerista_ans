# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Context Caching for Gemini 3.0 Pro
Implements cost optimization for repeated static content
"""

import datetime
import logging
import os
from typing import Optional

import vertexai
from vertexai.generative_models import GenerativeModel, Part
from vertexai.preview import caching

logger = logging.getLogger(__name__)


class ContextCacheManager:
    """
    Manages Gemini 3.0 context caching for static content.
    
    Use cases:
    - Large policy documents (LGPD, BACEN guidelines)
    - API documentation
    - Historical parecer templates
    - Technology standards and frameworks
    
    Cost savings: ~90% on cached input tokens
    """
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize cache manager.
        
        Args:
            project_id: Google Cloud project ID
            location: Region for Vertex AI (default: us-central1)
        """
        self.project_id = project_id
        self.location = location
        vertexai.init(project=project_id, location=location)
        self.active_caches = {}
        
    def create_policy_cache(
        self,
        cache_name: str,
        system_instruction: str,
        content_parts: list[Part],
        ttl_minutes: int = 60
    ) -> caching.CachedContent:
        """
        Create a cached context for policy documents and static content.
        
        Args:
            cache_name: Unique identifier for the cache
            system_instruction: System prompt to cache
            content_parts: List of Part objects (text, files, URIs)
            ttl_minutes: Time-to-live in minutes (default: 60)
            
        Returns:
            CachedContent object with resource handle
            
        Example:
            >>> manager = ContextCacheManager("my-project")
            >>> parts = [Part.from_uri("gs://bucket/lgpd_guidelines.pdf", "application/pdf")]
            >>> cache = manager.create_policy_cache(
            ...     "lgpd_policy_v1",
            ...     "Você é um especialista em LGPD...",
            ...     parts,
            ...     ttl_minutes=120
            ... )
        """
        try:
            cached_content = caching.CachedContent.create(
                model_name="gemini-3-pro-preview",
                system_instruction=system_instruction,
                contents=content_parts,
                ttl=datetime.timedelta(minutes=ttl_minutes),
                display_name=cache_name
            )
            
            self.active_caches[cache_name] = cached_content
            logger.info(
                f"Cache created: {cache_name} | "
                f"Resource ID: {cached_content.name} | "
                f"TTL: {ttl_minutes}min | "
                f"Expires: {cached_content.expire_time}"
            )
            
            return cached_content
            
        except Exception as e:
            logger.error(f"Failed to create cache '{cache_name}': {str(e)}")
            raise
    
    def get_model_with_cache(self, cache_name: str) -> GenerativeModel:
        """
        Get a GenerativeModel instance with cached content.
        
        Args:
            cache_name: Name of previously created cache
            
        Returns:
            GenerativeModel configured with cached content
            
        Raises:
            ValueError: If cache not found
        """
        if cache_name not in self.active_caches:
            raise ValueError(f"Cache '{cache_name}' not found. Create it first.")
        
        cached_content = self.active_caches[cache_name]
        
        model = GenerativeModel.from_cached_content(
            cached_content=cached_content
        )
        
        logger.info(f"Model instantiated with cache: {cache_name}")
        return model
    
    def update_cache_ttl(self, cache_name: str, new_ttl_minutes: int) -> None:
        """
        Extend TTL of an existing cache (keep-alive pattern).
        
        Args:
            cache_name: Name of cache to update
            new_ttl_minutes: New TTL in minutes
        """
        if cache_name not in self.active_caches:
            raise ValueError(f"Cache '{cache_name}' not found")
        
        cached_content = self.active_caches[cache_name]
        cached_content.update(ttl=datetime.timedelta(minutes=new_ttl_minutes))
        
        logger.info(f"Cache '{cache_name}' TTL extended to {new_ttl_minutes} minutes")
    
    def delete_cache(self, cache_name: str) -> None:
        """
        Manually delete a cache to stop incurring storage costs.
        
        Args:
            cache_name: Name of cache to delete
        """
        if cache_name not in self.active_caches:
            logger.warning(f"Cache '{cache_name}' not found, nothing to delete")
            return
        
        cached_content = self.active_caches[cache_name]
        cached_content.delete()
        del self.active_caches[cache_name]
        
        logger.info(f"Cache '{cache_name}' deleted")
    
    def list_caches(self) -> list[str]:
        """List all active cache names."""
        return list(self.active_caches.keys())
    
    @staticmethod
    def calculate_cache_roi(
        tokens_cached: int,
        queries_per_hour: int,
        ttl_hours: int,
        input_price_per_1k: float = 0.00125,  # Gemini 3.0 standard pricing
        cached_price_per_1k: float = 0.000125,  # ~10% of input
        storage_price_per_1k_per_hour: float = 0.0000005
    ) -> dict:
        """
        Calculate ROI for context caching.
        
        Args:
            tokens_cached: Number of tokens to cache
            queries_per_hour: Expected queries per hour
            ttl_hours: Cache lifetime in hours
            input_price_per_1k: Standard input token price
            cached_price_per_1k: Cached input token price
            storage_price_per_1k_per_hour: Storage cost per 1k tokens per hour
            
        Returns:
            Dictionary with cost analysis
        """
        tokens_1k = tokens_cached / 1000
        total_queries = queries_per_hour * ttl_hours
        
        # Cost without caching
        cost_no_cache = total_queries * tokens_1k * input_price_per_1k
        
        # Cost with caching
        creation_cost = tokens_1k * input_price_per_1k  # First creation
        storage_cost = tokens_1k * storage_price_per_1k_per_hour * ttl_hours
        query_cost = (total_queries - 1) * tokens_1k * cached_price_per_1k
        cost_with_cache = creation_cost + storage_cost + query_cost
        
        savings = cost_no_cache - cost_with_cache
        savings_percent = (savings / cost_no_cache * 100) if cost_no_cache > 0 else 0
        
        return {
            "cost_without_cache": round(cost_no_cache, 4),
            "cost_with_cache": round(cost_with_cache, 4),
            "savings_dollars": round(savings, 4),
            "savings_percent": round(savings_percent, 2),
            "break_even_queries": max(1, int(creation_cost / (tokens_1k * (input_price_per_1k - cached_price_per_1k)))),
            "recommendation": "USE_CACHE" if savings > 0 else "NO_CACHE"
        }


# Example usage pattern for the agent
def create_agent_with_policy_cache(project_id: str) -> GenerativeModel:
    """
    Example: Create an agent with LGPD policy documents cached.
    
    This reduces costs significantly for high-volume parecer processing.
    """
    manager = ContextCacheManager(project_id)
    
    # System instruction for the cached model
    system_instruction = """
    Você é um especialista em conformidade LGPD e BACEN para o setor financeiro.
    Analise requisições baseando-se exclusivamente nas políticas fornecidas.
    """
    
    # Example: Load static policy documents from GCS
    # In production, these would be actual policy PDFs
    content_parts = [
        Part.from_text("Políticas de LGPD e governança de dados do Banco BV..."),
        # Part.from_uri("gs://bv-policies/lgpd_guidelines.pdf", "application/pdf"),
        # Part.from_uri("gs://bv-policies/bacen_regulations.pdf", "application/pdf"),
    ]
    
    # Create cache with 2-hour TTL (adjust based on traffic patterns)
    cache = manager.create_policy_cache(
        cache_name="bv_compliance_policies_v1",
        system_instruction=system_instruction,
        content_parts=content_parts,
        ttl_minutes=120  # 2 hours
    )
    
    # Get model with cached content
    model = manager.get_model_with_cache("bv_compliance_policies_v1")
    
    # Calculate expected savings
    roi = ContextCacheManager.calculate_cache_roi(
        tokens_cached=50000,  # ~50k tokens of policy docs
        queries_per_hour=10,  # 10 parecer requests per hour
        ttl_hours=2
    )
    logger.info(f"Cache ROI: {roi}")
    
    return model

