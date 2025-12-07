# Gemini 3.0 Pro Migration Guide - Implementation Notes

## Overview

This document describes the implementation of recommendations from "Guia Técnico de Migração - Arquitetando Agentes de Próxima Geração com Gemini 3 Pro" for the Architecture Domain ANS Agent.

## Migration Date
December 2, 2025

## Key Changes Implemented

### 1. Model Configuration Update

**File**: `architecture_domain_ans/agent.py`

**Changes**:
- Updated model from `gemini-3-pro-preview` to `gemini-3.0-pro-001` (official release)
- Added `generation_config` with:
  - `thinking_level: "high"` - Enables deep reasoning for complex parecer analysis
  - `temperature: 1.0` - Uses default temperature for reasoning models (not 0.0)

**Rationale**: 
Gemini 3.0 is a Reasoning Engine, not a traditional LLM. It performs internal "System 2 thinking" before generating output. Low temperature restricts the model's ability to explore logical branches during this reasoning phase, degrading performance.

### 2. Optimized System Prompts

**New File**: `architecture_domain_ans/prompts_optimized.py`

**Changes**:
- Removed Chain-of-Thought instructions ("Pense passo a passo", "Explique seu raciocínio")
- Eliminated verbose prompt engineering "hacks"
- Focused on constraints, criteria, and expected outcomes
- Simplified structure for Gemini 3.0's native reasoning

**Rationale**:
Gemini 3.0 internalizes the reasoning process. Manual CoT prompts are redundant and can interfere with the model's native "Action over Thought" architecture. The model should be given objectives, not procedural instructions.

### 3. Context Caching Module

**New File**: `architecture_domain_ans/context_caching.py`

**Features**:
- `ContextCacheManager` class for managing cached content
- ROI calculator for cache cost analysis
- Support for large static content (policies, documentation)
- TTL management with keep-alive pattern

**Use Cases**:
- LGPD and BACEN policy documents (~50k tokens)
- Historical parecer templates
- Technology standards and frameworks
- API documentation

**Cost Savings**: Up to 90% reduction on repeated input tokens

**Example**:
```python
from architecture_domain_ans.context_caching import ContextCacheManager

manager = ContextCacheManager(project_id="gft-bu-gcp")

# Cache policy documents
parts = [Part.from_uri("gs://bv-policies/lgpd.pdf", "application/pdf")]
cache = manager.create_policy_cache(
    "lgpd_policies_v1",
    "Você é especialista em LGPD...",
    parts,
    ttl_minutes=120
)

# Use cached model
model = manager.get_model_with_cache("lgpd_policies_v1")
```

### 4. Thought Signature Handler

**New File**: `architecture_domain_ans/reasoning_handler.py`

**Features**:
- `ThoughtSignatureHandler` class for stateful reasoning preservation
- Proper function calling loop with signature propagation
- `ReasoningOrchestrator` for adaptive reasoning levels
- Tiered architecture support (router pattern)

**Critical Concept**:
When Gemini 3.0 invokes a function, it generates a `thoughtSignature` - an opaque token representing the reasoning path. This MUST be preserved and returned in the follow-up call, or the model suffers "reasoning amnesia".

**Example**:
```python
from architecture_domain_ans.reasoning_handler import ThoughtSignatureHandler

handler = ThoughtSignatureHandler(model, tools=[integrar_onetrust, consultar_cmdb])
handler.start_session()
response = handler.execute_reasoning_turn("Analise o fornecedor CNPJ 12345678000190")
```

## Architectural Patterns Implemented

### Pattern 1: Action over Thought
- No manual Chain-of-Thought in prompts
- Model handles reasoning internally
- thinking_level controls computation budget

### Pattern 2: Stateful Function Calling
- Thought signatures captured and propagated
- Reasoning context preserved across tool invocations
- Session-based conversation management

### Pattern 3: Context Caching
- Static content cached with TTL management
- Massive cost reduction for high-volume operations
- ROI calculation for optimal TTL tuning

### Pattern 4: Tiered Architecture (Recommended for Future)
```
User Request → Router (Fast Model)
                ├─> Low Complexity → Gemini 3.0 (thinking_level="low")
                └─> High Complexity → Gemini 3.0 (thinking_level="high")
```

## Function Schema Best Practices

### Critical Requirements for Gemini 3.0

1. **No $ symbols in JSON references**
   ```python
   # ❌ Wrong (OpenAI/OpenAPI style)
   {"$ref": "#/definitions/MyType"}
   
   # ✅ Correct (Vertex AI style)
   {"ref": "MyType"}
   ```

2. **Maximum nesting depth: 32 levels**
   Deep object hierarchies may need flattening

3. **Recursion depth limit: 2**
   Self-referencing schemas must be shallow

4. **Descriptions are functionally mandatory**
   ```python
   # ❌ Poor (will degrade reasoning)
   {"type": "string", "name": "cnpj"}
   
   # ✅ Good (enables semantic understanding)
   {
       "type": "string",
       "name": "cnpj",
       "description": "CNPJ do fornecedor no formato 14 dígitos numéricos"
   }
   ```

## Migration Checklist

- [x] Update model name to `gemini-3.0-pro-001`
- [x] Add `thinking_level` configuration
- [x] Set temperature to 1.0 (or remove parameter)
- [x] Create optimized prompts (remove CoT)
- [x] Implement context caching module
- [x] Implement thought signature handler
- [ ] Validate all function schemas (no $, proper descriptions)
- [ ] Test with production parecer workloads
- [ ] Measure latency P95/P99 baselines
- [ ] Calculate cache ROI for actual traffic
- [ ] Update documentation and team training

## Testing Strategy

### Phase 1: Validation (Week 1)
- Unit tests with new configuration
- Compare outputs with legacy model
- Measure latency differences (expecting 10-20s pause for high reasoning)

### Phase 2: Integration (Week 2)
- End-to-end tests with real CNPJ data
- Validate thought signature preservation
- Test function calling loops

### Phase 3: Performance (Week 3)
- Load testing with production-like volume
- Cache hit rate measurement
- Cost analysis

## Expected Outcomes

### Latency
- **Low complexity tasks**: Near instant (thinking_level="low")
- **High complexity parecer analysis**: 10-20 seconds initial thinking, then fast generation
- **With caching**: 50-70% reduction in input processing time

### Cost
- **Without cache**: Standard Gemini 3.0 pricing
- **With cache (typical usage)**: 60-90% reduction on input tokens
- **Break-even point**: ~5-10 queries per cached content

### Quality
- Reduced hallucinations due to deeper reasoning
- More consistent parecer criteria application
- Better handling of edge cases

## Troubleshooting

### Issue: "Model takes too long to respond"
**Solution**: This is expected with `thinking_level="high"`. The model is performing deep reasoning. For fast responses on simple queries, use adaptive routing or set to "low".

### Issue: "Function calling results are inconsistent"
**Solution**: Ensure thought signatures are being captured and propagated. Check `reasoning_handler.py` implementation.

### Issue: "Cache not providing cost savings"
**Solution**: 
1. Check queries per hour vs TTL
2. Use ROI calculator to optimize TTL
3. Ensure content is truly static (>1024 tokens)

## References

1. Gemini 3 Developer Guide: https://ai.google.dev/gemini-api/docs/gemini-3
2. Vertex AI Function Calling: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/function-calling
3. Context Caching Overview: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/context-cache/context-cache-overview

## Next Steps

1. **Prompt Optimization with VAPO** (Vertex AI Prompt Optimizer)
   - Extract 100 high-quality parecer examples
   - Run optimization jobs to mathematically tune prompts
   - A/B test optimized vs manual prompts

2. **Production Monitoring**
   - Add latency tracking (P95, P99)
   - Monitor cache hit rates
   - Track cost per parecer
   - Alert on reasoning failures

3. **Team Training**
   - Share migration guide with team
   - Demonstrate new patterns (caching, thought signatures)
   - Update internal documentation

4. **Continuous Improvement**
   - Collect feedback from parecer results
   - Fine-tune thinking_level thresholds
   - Optimize cache TTLs based on actual traffic
   - Consider multi-model routing for cost optimization

## Contact

For questions about this migration, contact the Architecture Team.

---
*Document Version: 1.0*  
*Last Updated: December 2, 2025*

