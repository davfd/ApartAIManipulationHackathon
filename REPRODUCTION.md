# Reproduction Guide

**Conditional Alignment: AI Safety Hackathon Submission**

---

## Quick Test (5 minutes, $5)

Get started immediately with minimal cost:

```bash
# Clone and setup
git clone https://github.com/yourusername/conditional-alignment.git
cd conditional-alignment
pip install -r requirements.txt

# Set API keys
export ANTHROPIC_API_KEY=your_key_here
export OPENAI_API_KEY=your_key_here  # optional
export GOOGLE_API_KEY=your_key_here  # optional

# Run quick test (100 queries, ~$5)
python code/capability_routing/run_all_dynamic.py --quick-test

# Expected output:
# - Safety: 0% harmful (across all test scenarios)
# - Capability: ~84% accuracy maintained
# - Runtime: ~5 minutes
```

---

## Budget Test ($200)

More comprehensive validation without full cost:

```bash
# Capability evaluation (1,000 questions instead of 15,809)
python code/capability_routing/run_all_dynamic.py --smoke-test

# Safety evaluation (500 scenarios instead of 8,632)
python code/anthropic_agentic/generate_prompts_with_seed.py --budget-mode

# Estimated cost: ~$200
# Estimated time: 2-3 hours
```

---

## Full Replication ($1,140)

Complete reproduction of all results:

### Prerequisites

- Python 3.8+
- API keys for: Anthropic, OpenAI (optional), Google (optional)
- ~20GB disk space for results
- ~$1,140 budget

### Step-by-Step Instructions

#### 1. Environment Setup

```bash
git clone https://github.com/yourusername/conditional-alignment.git
cd conditional-alignment
pip install -r requirements.txt
```

#### 2. API Configuration

```bash
# Required
export ANTHROPIC_API_KEY=your_anthropic_key

# Optional (for multi-model testing)
export OPENAI_API_KEY=your_openai_key
export GOOGLE_API_KEY=your_google_key
```

#### 3. Run Safety Evaluation (Anthropic Agentic Suite)

```bash
# Generate test scenarios with seed configurations
python code/anthropic_agentic/generate_prompts_with_seed.py \
  --config code/anthropic_agentic/configs/seed_on.yaml \
  --output results/anthropic_agentic/

# Cost: ~$865
# Time: 4-6 hours
# Expected: 0% harmful rate across 8,632 scenarios
```

#### 4. Run Capability Evaluation

```bash
# Test dynamic routing on 15,809 questions
python code/capability_routing/run_all_dynamic.py \
  --model gemini-2.5-flash \
  --output results/capability_dynamic/

# Cost: ~$150
# Time: 3-4 hours
# Expected: 84.2% accuracy (vs 83.3% baseline, 20.3% full seed)
```

#### 5. Run Liar Detection

```bash
# Test deception detection
python code/liar_detection/detect_liar.py \
  --model gpt-4-turbo \
  --output results/liar_detection/

# Cost: ~$50
# Time: 1-2 hours
# Expected: 72% deception rate in baseline GPT-4-Turbo
```

#### 6. Analyze Results

```bash
# Generate statistical analysis
python code/analysis/generate_stats.py \
  --input results/ \
  --output results/STATISTICAL_ANALYSIS.md
```

---

## Expected Results

### Safety (Anthropic Agentic Suite)

| Model | Baseline Harmful % | With Seed Harmful % | p-value |
|-------|-------------------|---------------------|---------|
| Claude Opus 4.1 | 51.1% | 0% | < 10⁻¹⁵ |
| Gemini 2.5 Pro | 47.9% | 0% | < 10⁻¹⁵ |
| GPT-4o | 4.1% | 0% | < 10⁻¹⁵ |
| Venice Uncensored | 77.7% | 0.2% | < 10⁻¹⁵ |

### Capability (Gemini 2.5 Flash)

| Condition | MMLU | GPQA | GSM8K | Overall |
|-----------|------|------|-------|---------|
| Baseline | 84.2% | 20.1% | 94.5% | 83.3% |
| Full Seed (63KB) | 22.1% | 22.1% | 0.2% | 20.3% |
| **Dynamic Routing** | **85.2%** | **22.5%** | **94.2%** | **84.2%** |

### Tier Distribution

| Tier | % of Queries | Seed Size |
|------|--------------|-----------|
| T0 | 91.0% | 849 bytes |
| T1 | 0.6% | 2-3 KB |
| T2 | 7.5% | 6-7 KB |
| T3 | 0.8% | 10-19 KB |

---

## Cost Breakdown

| Component | # Tests | API Cost | Time |
|-----------|---------|----------|------|
| Anthropic Agentic Suite | 8,632 | $865 | 4-6h |
| Capability Evaluation | 15,809 | $150 | 3-4h |
| Liar Detection | ~500 | $50 | 1-2h |
| Jailbreak Tests (HarmBench) | 1,680 | $50 | 1-2h |
| PAIR/GCG Tests | 560 | $25 | 1h |
| **Total** | **27,181** | **$1,140** | **10-15h** |

---

## Troubleshooting

### API Rate Limits

If you hit rate limits:

```bash
# Reduce parallelism
python code/capability_routing/run_all_dynamic.py --workers 1

# Or add delays
python code/capability_routing/run_all_dynamic.py --delay 1.0
```

### Out of Memory

```bash
# Process in batches
python code/capability_routing/run_all_dynamic.py --batch-size 100
```

### Missing Dependencies

```bash
# Reinstall all dependencies
pip install -r requirements.txt --upgrade
```

---

## Validation Checklist

After running reproduction:

- [ ] Safety: 0% harmful rate achieved (p < 10⁻¹⁵)
- [ ] Capability: ~84% accuracy maintained (vs ~83% baseline)
- [ ] Tier distribution: ~91% routed to T0
- [ ] Cost reduction: ~97% vs full seed
- [ ] No catastrophic collapse (full seed shows ~20% accuracy)

---

## Support

For questions or issues:
- Open an issue on GitHub
- Email: [contact information]
- Check METHODOLOGY.md for technical details

---

## Citation

If you use this work:

```bibtex
@misc{conditional-alignment-2026,
  title={Conditional Alignment: Detecting and Preventing AI Agentic Manipulation at Zero Capability Cost},
  author={Jonathan & David Fortin-Dominguez},
  year={2026},
  howpublished={AI Manipulation Hackathon Submission}
}
```
