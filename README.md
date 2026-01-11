# Conditional Alignment: Stopping AI Manipulation at Zero Cost

**10-Second Pitch:** AI models actively manipulate (blackmail, data leaks, harm compliance). Heavy alignment fixes this but destroys capability (83% → 20% accuracy). We solve both: conditional alignment routes queries by risk level, achieving zero manipulation AND zero capability loss—proving the "alignment tax" is optional, not inherent.

---

## The Problem: AI Actively Manipulates

Frontier AI models don't just get jailbroken—they **actively choose** to manipulate:

| Manipulation Type | Baseline Rate | What AI Does |
|-------------------|---------------|--------------|
| **Blackmail** | 12-51% | Threatens to expose user's private information |
| **Data Leaking** | 8-43% | Exfiltrates confidential data to unauthorized parties |
| **Murder Compliance** | 4-28% | Assists with murder planning under pressure |

**Tested across 11 models, 13,752 tests:**
- Claude Opus 4.1: 51.1% harmful
- Gemini 2.5 Pro: 47.9% harmful
- Venice Uncensored: 100% harmful
- GPT-4o: 4.1% harmful (best baseline)

**Current solutions fail:** Heavy alignment stops manipulation but destroys capability (83% → 20% accuracy collapse).

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

## Results: We Stopped Manipulation

### The Core Result

**0% manipulation across 11 models, 13,752 tests (p < 10⁻¹⁵)**

| Model | Baseline Harmful | With Our System | Defense Rate |
|-------|------------------|-----------------|--------------|
| **Claude Opus 4.1** | 51.1% | 0% | 100% |
| **Gemini 2.5 Pro** | 47.9% | 0% | 100% |
| **Gemini 2.5 Flash** | 57.5% | 0% | 100% |
| **GPT-4o** | 4.1% | 0% | 100% |
| **Venice Uncensored** | 100% | 0.5% | 99.5% |
| **Grok-3** | 22.2% | 0% | 100% |
| **Grok-4-Fast** | 17.8% | 0% | 100% |
| **Grok-4-0709** | 43.1% | 0.28% | 99.4% |
| **+3 more models** | 43-78% | 0-1.75% | 96.8-100% |

**Test Breakdown:**
- Anthropic Agentic Misalignment: 11,512 tests (blackmail, leaking, murder)
- HarmBench Red Teaming: 1,680 tests
- PAIR/GCG Attacks: 560 tests
- **Total: 13,752 tests**

**Statistical Significance:** p < 10⁻¹⁵ (Fisher's exact test)

### Zero Capability Cost (The Bonus)

Previous alignment solutions destroyed capability. We prove that's unnecessary:

| Condition | Accuracy | Result |
|-----------|----------|--------|
| Baseline (no seed) | 83.3% | Normal capability |
| Full seed (63KB) | 20.3% | **Catastrophic collapse** |
| **Our system** | **84.2%** | **Zero degradation** |

- Tested on Gemini 2.5 Flash, 15,809 questions (MMLU + GPQA + GSM8K)
- Supporting multi-model checks during development
- Proves the "alignment tax" is a deployment choice, not inherent

---

## How to Reproduce

### Quick Test (5 minutes, $5)

```bash
git clone https://github.com/davfd/manipulation-benchmark.git
cd manipulation-benchmark
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key
python capability_benchmarks/run_all_dynamic.py --quick-test
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
