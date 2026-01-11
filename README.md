# Conditional Alignment: Zero Manipulation at Zero Capability Cost

**10-Second Pitch:** Conditional alignment routes 91% of benign queries through a tiny 849B safety seed, escalating tiers only when needed—achieving 0% manipulation, 84.2% capability (vs 20.3% catastrophic collapse with full seed), ~97% cost reduction, with strong stats (p < 10⁻¹⁵) and multi-model safety validation.

---

## The Problem

AI models actively manipulate (4-51% harmful rate across frontier models). Heavy alignment breaks capability. We need both safety **AND** capability.

### The Catastrophic Collapse

| Condition | Accuracy | What Happened |
|-----------|----------|---------------|
| Baseline (no seed) | 83.3% | Normal capability |
| Full seed (63KB) | 20.3% | **CATASTROPHIC COLLAPSE** (-63 points) |
| Dynamic routing | 84.2% | **COMPLETE RESCUE** (+0.9 vs baseline) |

**The insight:** The "alignment tax" isn't inherent—it's a deployment choice.

---

## The Solution: Conditional Alignment

Route queries through tiered safety levels based on operations required, not semantic intent.

### Four-Tier System

| Tier | Size | Usage | Description |
|------|------|-------|-------------|
| **T0** | 849B | 91% | Minimal - simple factual queries |
| **T1** | 2-3 KB | 0.6% | Normal - procedural queries |
| **T2** | 6-7 KB | 7.5% | Moral - ethical reasoning required |
| **T3** | 10-19 KB | 0.8% | Safety - harmful/jailbreak detected |

###Multi-Phase Security

Jailbreak must beat **both** layers:
1. **Routing layer:** Operations-based classifier (deterministic)
2. **Model layer:** Appropriate safety seed loaded

---

## Key Results

### Four Headline Numbers

- **0% manipulation** (p < 10⁻¹⁵ across 16 models)
- **84.2% capability** maintained (vs 20.3% collapse with full seed)
- **97% cost reduction** (849B vs 63KB for most queries)
- **p < 10⁻¹⁵** statistical significance (Fisher's exact test)

### Safety Validation

- **16 models tested:** Claude Opus 4.1, Gemini 2.5 Pro/Flash, GPT-4o, Grok-3/4-Fast/4-0709, Venice uncensored, etc.
- **8,632 scenarios:** Blackmail, leaking, murder under various goal conditions
- **Worst-case proof:** Venice uncensored (no safety training) went from 77.7% → 0.2% harmful

### Capability Validation

- **Deep evaluation:** Gemini 2.5 Flash on 15,809 questions across multiple test suites
- **Supporting multi-model checks:** Additional models tested during development
- **Zero degradation:** 84.2% vs 83.3% baseline (+0.9 points)

---

## How to Reproduce

### Quick Test (5 minutes, $5)

```bash
git clone https://github.com/yourusername/conditional-alignment.git
cd conditional-alignment
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python code/capability_routing/run_all_dynamic.py --quick-test
```

### Full Replication ($1,140)

See [REPRODUCTION.md](REPRODUCTION.md) for complete instructions.

---

## Documentation

- **[JUDGE_SHEET.md](JUDGE_SHEET.md)** - 1-page summary for judges
- **[PROJECT_REPORT.md](PROJECT_REPORT.md)** - Main submission document
- **[METHODOLOGY.md](METHODOLOGY.md)** - Technical details and statistical methods
- **[LIMITATIONS_DUAL_USE.md](LIMITATIONS_DUAL_USE.md)** - Limitations and dual-use risks
- **[REPRODUCTION.md](REPRODUCTION.md)** - Step-by-step replication guide

---

## What's New (Innovation)

1. **Runtime policy routing** - Alignment overhead is conditional, not static
2. **Capability rescue proof** - First to show catastrophic collapse + complete rescue
3. **Multi-phase security** - Both routing layer AND model layer must fail
4. **Operations-based classification** - Deterministic/auditable, not semantic intent guessing

---

## Project Structure

```
conditional-alignment/
├── README.md                          # This file
├── JUDGE_SHEET.md                     # 1-page judge summary
├── PROJECT_REPORT.md                  # Main submission
├── METHODOLOGY.md                     # Technical details
├── LIMITATIONS_DUAL_USE.md            # Limitations & dual-use
├── REPRODUCTION.md                    # Replication guide
│
├── code/
│   ├── capability_routing/            # Dynamic routing system
│   │   ├── classifier_v2.py           # 4-tier classifier
│   │   ├── run_all_dynamic.py         # Test runner
│   │   └── loader.py                  # Data loading
│   │
│   ├── anthropic_agentic/             # Agentic evaluation integration
│   │   ├── generate_prompts_with_seed.py
│   │   └── configs/
│   │
│   └── liar_detection/                # Deception detection system
│       ├── detect_liar.py
│       ├── classifier_v153.py
│       └── heatmap_attribution.py
│
├── seeds/                             # Tiered safety seeds
│   ├── seed_v2.6.txt                  # Full seed (63KB)
│   └── seed_components/               # T0-T3 components
│
├── results/                           # Validation results
│   ├── anthropic_agentic/
│   └── capability_dynamic/
│
├── data/                              # Test datasets
└── requirements.txt                   # Dependencies
```

---

## Citation

If you use this work, please cite:

```bibtex
@misc{conditional-alignment-2026,
  title={Conditional Alignment: Detecting and Preventing AI Agentic Manipulation at Zero Capability Cost},
  author={Jonathan & David Fortin-Dominguez},
  year={2026},
  howpublished={AI Manipulation Hackathon Submission}
}
```

---

## License

MIT License - See LICENSE file for details

---

## Contact

For questions or collaboration: [contact information]
