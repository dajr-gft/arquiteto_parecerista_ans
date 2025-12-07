#!/usr/bin/env python3
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
Example: Gemini 3.0 Pro Features Demonstration
Shows new capabilities: Context Caching, Thought Signatures, Adaptive Reasoning
"""

import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT', 'gft-bu-gcp')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')


def example_1_basic_reasoning():
    """
    Example 1: Basic agent usage with Gemini 3.0 reasoning

    Demonstrates:
    - thinking_level="high" for deep analysis
    - No manual Chain-of-Thought needed
    - Natural function calling
    """
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Reasoning with Gemini 3.0")
    print("="*80 + "\n")

    from architecture_domain_ans.agent import root_agent

    print("Agent Configuration:")
    print(f"  Model: {root_agent.model}")
    print(f"  Thinking Level: high (deep reasoning enabled)")
    print(f"  Temperature: 1.0 (default for reasoning)")

    print("\nNote: With thinking_level='high', expect 10-20s initial pause")
    print("      This is the model performing deep reasoning before responding.\n")

    # Example query
    query = """
    Analise o seguinte cenário:
    - Fornecedor: Tech Solutions LTDA (CNPJ: 12.345.678/0001-90)
    - Tipo: Renovação de contrato
    - Serviço: API de Consulta de Crédito (api_id: credit-api-v2)
    - Integrações: REST, Webhook
    - Armazena dados BV: Sim
    """

    print(f"Query: {query}\n")
    print("Processing... (model is thinking deeply about the parecer criteria)")

    # In real usage, you would call the agent here
    # response = root_agent.run(query)
    print("\n[Simulated Response - In production, agent would analyze using all tools]")


def example_2_context_caching():
    """
    Example 2: Context Caching for cost optimization

    Demonstrates:
    - Caching large policy documents
    - ROI calculation
    - TTL management
    """
    print("\n" + "="*80)
    print("EXAMPLE 2: Context Caching for Policy Documents")
    print("="*80 + "\n")

    from architecture_domain_ans.context_caching import ContextCacheManager
    from vertexai.generative_models import Part

    manager = ContextCacheManager(PROJECT_ID, LOCATION)

    # Calculate ROI first
    print("ROI Analysis for caching LGPD policy documents:")
    roi = ContextCacheManager.calculate_cache_roi(
        tokens_cached=50000,  # 50k tokens of policy docs
        queries_per_hour=10,   # 10 parecer requests/hour
        ttl_hours=2            # 2 hour cache lifetime
    )

    print(f"  Tokens to cache: 50,000")
    print(f"  Expected queries: 10/hour for 2 hours = 20 total")
    print(f"  Cost without cache: ${roi['cost_without_cache']}")
    print(f"  Cost with cache: ${roi['cost_with_cache']}")
    print(f"  Savings: ${roi['savings_dollars']} ({roi['savings_percent']}%)")
    print(f"  Recommendation: {roi['recommendation']}")
    print(f"  Break-even: {roi['break_even_queries']} queries\n")

    # Create cache (example with text, in production use GCS URIs)
    print("Creating cache for LGPD policies...")

    system_instruction = """
    Você é especialista em LGPD e conformidade para instituições financeiras.
    Analise requisições baseando-se nas políticas do Banco BV fornecidas.
    """

    content_parts = [
        Part.from_text("""
        [Simulação de Políticas LGPD do Banco BV]
        
        1. Armazenamento de dados por terceiros requer:
           - Data Processing Agreement (DPA)
           - Certificações ISO 27001 e SOC 2
           - Auditoria anual de segurança
        
        2. Dados sensíveis devem ter:
           - Criptografia em trânsito (TLS 1.3+)
           - Criptografia em repouso (AES-256)
           - Logs de acesso com retenção de 5 anos
        
        [... 47,000 tokens adicionais ...]
        """)
    ]

    try:
        cache = manager.create_policy_cache(
            cache_name="lgpd_policies_demo",
            system_instruction=system_instruction,
            content_parts=content_parts,
            ttl_minutes=120
        )
        print(f"✓ Cache created: {cache.name}")
        print(f"  Expires: {cache.expire_time}")

        # Get model with cache
        model = manager.get_model_with_cache("lgpd_policies_demo")
        print(f"✓ Model configured with cached content")

        # Example query (would use cached context)
        print("\nExample query using cached policies:")
        print("  'Fornecedor X armazena dados BV. Está em conformidade?'")
        print("  → Model would analyze using cached LGPD policies")
        print("  → Cost: ~90% less than without cache\n")

        # Cleanup
        manager.delete_cache("lgpd_policies_demo")
        print("✓ Cache deleted (stopping storage costs)")

    except Exception as e:
        logger.error(f"Cache example failed: {e}")
        print(f"Note: Full cache example requires Vertex AI access")


def example_3_thought_signatures():
    """
    Example 3: Thought Signature handling for stateful reasoning

    Demonstrates:
    - Proper function calling with reasoning preservation
    - Multi-step analysis workflow
    """
    print("\n" + "="*80)
    print("EXAMPLE 3: Thought Signatures and Stateful Reasoning")
    print("="*80 + "\n")

    print("Gemini 3.0 Critical Concept: Thought Signatures")
    print("-" * 80)
    print("""
    When Gemini 3.0 calls a function, it generates a 'thoughtSignature':
    - Opaque token representing the reasoning path
    - MUST be preserved and returned in follow-up
    - Without it, model loses cognitive context ("reasoning amnesia")
    
    Example flow:
    1. User: "Analise fornecedor X"
    2. Model thinks → decides to call integrar_onetrust(cnpj="123")
    3. Model generates: functionCall + thoughtSignature
    4. System executes function → gets result
    5. System returns: functionResponse + original thoughtSignature ✓
    6. Model continues reasoning with full context
    """)

    print("\nImplementation:")
    print("  See: architecture_domain_ans/reasoning_handler.py")
    print("  Class: ThoughtSignatureHandler")
    print("  Method: execute_reasoning_turn()\n")

    # Show conceptual code
    print("Conceptual code:")
    print("""
    handler = ThoughtSignatureHandler(model, tools)
    handler.start_session()
    
    # Model will:
    # 1. Reason about the task
    # 2. Call functions as needed (with signatures preserved)
    # 3. Synthesize final answer
    response = handler.execute_reasoning_turn(
        "Analise parecer para fornecedor CNPJ 12345678000190"
    )
    """)


def example_4_adaptive_reasoning():
    """
    Example 4: Adaptive reasoning with tiered architecture

    Demonstrates:
    - Complexity-based routing
    - thinking_level switching
    - Cost optimization
    """
    print("\n" + "="*80)
    print("EXAMPLE 4: Adaptive Reasoning (Tiered Architecture)")
    print("="*80 + "\n")

    from architecture_domain_ans.reasoning_handler import ReasoningOrchestrator

    print("Concept: Route queries based on complexity\n")

    orchestrator_low = ReasoningOrchestrator(
        PROJECT_ID, LOCATION, thinking_level="low"
    )
    orchestrator_high = ReasoningOrchestrator(
        PROJECT_ID, LOCATION, thinking_level="high"
    )

    # Example tasks with complexity scores
    tasks = [
        {
            "prompt": "Qual é o status do fornecedor X?",
            "complexity": 2,
            "description": "Simple lookup"
        },
        {
            "prompt": "Analise histórico completo e sugira parecer",
            "complexity": 9,
            "description": "Complex multi-criteria analysis"
        },
    ]

    for i, task in enumerate(tasks, 1):
        print(f"Task {i}: {task['prompt']}")
        print(f"  Complexity: {task['complexity']}/10 - {task['description']}")

        should_think_deep = orchestrator_low.should_use_high_reasoning(
            task['complexity']
        )

        recommended = "HIGH" if should_think_deep else "LOW"
        print(f"  Recommended thinking_level: {recommended}")

        if should_think_deep:
            print(f"  → Route to Gemini 3.0 with thinking_level='high'")
            print(f"     Expect: 10-20s deep reasoning, high quality")
        else:
            print(f"  → Route to Gemini 3.0 with thinking_level='low'")
            print(f"     Expect: Near instant response, good quality")
        print()

    print("Benefits of Tiered Architecture:")
    print("  ✓ Cost optimization (fast responses don't pay for deep reasoning)")
    print("  ✓ Better UX (instant responses when possible)")
    print("  ✓ Resource efficiency (computation matches task needs)")


def example_5_migration_comparison():
    """
    Example 5: Before/After migration comparison

    Shows the differences between GPT-4 and Gemini 3.0 approaches
    """
    print("\n" + "="*80)
    print("EXAMPLE 5: Migration Comparison (GPT-4 → Gemini 3.0)")
    print("="*80 + "\n")

    print("PROMPT ENGINEERING")
    print("-" * 80)

    print("\n❌ GPT-4 Approach (Verbose, Manual CoT):")
    print("""
    \"\"\"
    Você é um analista de arquitetura.
    
    Pense passo a passo:
    1. Primeiro, analise o CNPJ
    2. Depois, consulte o OneTrust
    3. Em seguida, verifique o CMDB
    4. Explique seu raciocínio antes de responder
    5. Se não souber, diga "Não sei"
    
    Certifique-se de:
    - Verificar cada campo
    - Documentar cada decisão
    - Mostrar seu processo de pensamento
    \"\"\"
    """)

    print("\n✅ Gemini 3.0 Approach (Concise, Outcome-focused):")
    print("""
    \"\"\"
    Você é um Analista Sênior de Arquitetura do Banco BV.
    
    Analise requisições de parecer considerando:
    - Conformidade (OneTrust, LGPD, BACEN)
    - Direcionamento estratégico (CMDB)
    - Histórico e riscos
    
    Retorne JSON estruturado com parecer_sugerido e justificativa.
    \"\"\"
    """)

    print("\n" + "-" * 80)
    print("CONFIGURATION")
    print("-" * 80)

    print("\n❌ GPT-4 Configuration:")
    print("  model: gpt-4")
    print("  temperature: 0.0  # Low for determinism")
    print("  top_p: 0.1")

    print("\n✅ Gemini 3.0 Configuration:")
    print("  model: gemini-3.0-pro-001")
    print("  generation_config:")
    print("    thinking_level: high  # Deep reasoning")
    print("    temperature: 1.0      # Default for reasoning")

    print("\n" + "-" * 80)
    print("FUNCTION CALLING")
    print("-" * 80)

    print("\n❌ GPT-4: Stateless, no reasoning preservation")
    print("  Call function → Return result → Model continues")

    print("\n✅ Gemini 3.0: Stateful with thought signatures")
    print("  Call function WITH signature →")
    print("  Return result WITH signature →")
    print("  Model continues with full reasoning context")

    print("\n" + "-" * 80)
    print("PERFORMANCE CHARACTERISTICS")
    print("-" * 80)

    print("\nGPT-4:")
    print("  Latency: Consistent, ~2-5s")
    print("  Quality: Good with extensive prompt engineering")
    print("  Cost: Standard per-token pricing")

    print("\nGemini 3.0:")
    print("  Latency: 10-20s for high reasoning (worth it!), instant for low")
    print("  Quality: Better with less prompt engineering")
    print("  Cost: Lower with context caching (60-90% reduction)")


def main():
    """Run all examples."""
    print("\n" + "="*80)
    print("GEMINI 3.0 PRO - NEW FEATURES DEMONSTRATION")
    print("Architecture Domain ANS Agent")
    print("="*80)

    examples = [
        ("Basic Reasoning", example_1_basic_reasoning),
        ("Context Caching", example_2_context_caching),
        ("Thought Signatures", example_3_thought_signatures),
        ("Adaptive Reasoning", example_4_adaptive_reasoning),
        ("Migration Comparison", example_5_migration_comparison),
    ]

    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nRunning all examples...\n")

    for name, func in examples:
        try:
            func()
        except Exception as e:
            logger.error(f"Example '{name}' failed: {e}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("""
Key Takeaways:

1. Gemini 3.0 is a REASONING ENGINE, not just an LLM
   → Use thinking_level to control computation budget
   → Remove manual Chain-of-Thought prompts

2. Context Caching provides massive cost savings
   → 60-90% reduction for repeated content
   → Critical for high-volume production workloads

3. Thought Signatures are MANDATORY for correct function calling
   → Preserve reasoning context across tool invocations
   → Use ThoughtSignatureHandler for proper implementation

4. Tiered Architecture optimizes cost and latency
   → Route simple queries to low reasoning
   → Route complex analysis to high reasoning

5. Temperature=1.0 is correct for reasoning models
   → Low temperature restricts reasoning exploration
   → Let the model manage its own entropy

Next Steps:
- Review GEMINI_3_MIGRATION.md for full details
- Test with production data
- Monitor latency and cost metrics
- Optimize cache TTLs based on traffic patterns
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()

