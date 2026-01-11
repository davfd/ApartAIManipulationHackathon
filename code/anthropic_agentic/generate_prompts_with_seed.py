#!/usr/bin/env python3
"""
Foundation Alignment - Anthropic Agentic Misalignment Integration

This script wraps the official anthropic-experimental/agentic-misalignment
prompt generator to inject Foundation Alignment Seeds into system prompts.

Usage:
    python generate_prompts_with_seed.py --config configs/experiment.yaml --seed ../../seeds/seed_v2.6.txt

Prerequisites:
    1. Clone the official repo:
       git clone https://github.com/anthropic-experimental/agentic-misalignment external/agentic-misalignment
    2. Install requirements:
       pip install -r external/agentic-misalignment/requirements.txt
"""

import sys
import argparse
import yaml
from pathlib import Path


def inject_seed_to_prompts(experiment_dir: Path, seed_path: Path, verbose: bool = True):
    """
    Prepend Foundation Alignment Seed to all system_prompt.txt files in experiment.

    The Anthropic agentic-misalignment framework stores prompts in this structure:
    results/[experiment_id]/prompts/[condition]/system_prompt.txt

    This function finds all system_prompt.txt files and prepends the seed content.
    """

    with open(seed_path, 'r', encoding='utf-8') as f:
        seed_content = f.read()

    if verbose:
        print(f"Loaded seed from {seed_path} ({len(seed_content)} chars)")

    # Find all condition directories containing system prompts
    prompts_dir = experiment_dir / "prompts"
    if not prompts_dir.exists():
        print(f"ERROR: Prompts directory not found: {prompts_dir}")
        print("Make sure you've run the official generate_prompts.py first.")
        return 0

    modified_count = 0

    # Walk through all subdirectories looking for system_prompt.txt
    for system_prompt_file in prompts_dir.glob("**/system_prompt.txt"):
        with open(system_prompt_file, 'r', encoding='utf-8') as f:
            original_prompt = f.read()

        # Check if seed already injected (prevent double-injection)
        if "FOUNDATION ALIGNMENT SEED" in original_prompt:
            if verbose:
                print(f"  SKIP (already has seed): {system_prompt_file.relative_to(experiment_dir)}")
            continue

        # Prepend seed with clear separator
        modified_prompt = f"""═══════════════════════════════════════════════════════════
FOUNDATION ALIGNMENT SEED - INJECTED FOR SAFETY EVALUATION
═══════════════════════════════════════════════════════════

{seed_content}

═══════════════════════════════════════════════════════════
ORIGINAL SYSTEM PROMPT BELOW
═══════════════════════════════════════════════════════════

{original_prompt}"""

        with open(system_prompt_file, 'w', encoding='utf-8') as f:
            f.write(modified_prompt)

        modified_count += 1
        if verbose:
            print(f"  INJECTED: {system_prompt_file.relative_to(experiment_dir)}")

    return modified_count


def main():
    parser = argparse.ArgumentParser(
        description="Inject Foundation Alignment Seed into Anthropic Agentic Misalignment prompts"
    )
    parser.add_argument(
        "--config",
        required=True,
        help="Path to experiment config YAML file"
    )
    parser.add_argument(
        "--seed",
        required=True,
        help="Path to Foundation Alignment Seed file"
    )
    parser.add_argument(
        "--skip-generate",
        action="store_true",
        help="Skip prompt generation (only inject seed into existing prompts)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )

    args = parser.parse_args()
    verbose = not args.quiet

    # Validate paths
    config_path = Path(args.config)
    seed_path = Path(args.seed)

    if not config_path.exists():
        print(f"ERROR: Config file not found: {config_path}")
        sys.exit(1)

    if not seed_path.exists():
        print(f"ERROR: Seed file not found: {seed_path}")
        sys.exit(1)

    # Load config to get experiment_id
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    experiment_id = config.get('experiment_id', 'default_experiment')

    if verbose:
        print("=" * 60)
        print("FOUNDATION ALIGNMENT - SEED INJECTION")
        print("=" * 60)
        print(f"Experiment ID: {experiment_id}")
        print(f"Config: {config_path}")
        print(f"Seed: {seed_path}")
        print()

    # Step 1: Generate prompts using official script (unless skipped)
    if not args.skip_generate:
        if verbose:
            print("[Step 1/2] Generating base prompts...")

        # Try to import and run the official generate_prompts
        external_path = Path("external/agentic-misalignment")
        if not external_path.exists():
            print(f"ERROR: Official repo not found at {external_path}")
            print("Please clone it first:")
            print("  git clone https://github.com/anthropic-experimental/agentic-misalignment external/agentic-misalignment")
            sys.exit(1)

        sys.path.insert(0, str(external_path))

        try:
            from scripts.generate_prompts import generate_prompts_from_yaml
            generate_prompts_from_yaml(str(config_path))
            if verbose:
                print("  Base prompts generated successfully")
        except ImportError as e:
            print(f"ERROR: Could not import official generate_prompts: {e}")
            print("Make sure you've installed the requirements:")
            print("  pip install -r external/agentic-misalignment/requirements.txt")
            sys.exit(1)
        except Exception as e:
            print(f"ERROR: Prompt generation failed: {e}")
            sys.exit(1)
    else:
        if verbose:
            print("[Step 1/2] Skipping prompt generation (--skip-generate)")

    # Step 2: Inject seed into all system prompts
    if verbose:
        print()
        print("[Step 2/2] Injecting Foundation Alignment Seed...")

    experiment_dir = Path(f"results/{experiment_id}")
    if not experiment_dir.exists():
        print(f"ERROR: Experiment directory not found: {experiment_dir}")
        print("Make sure prompt generation completed successfully.")
        sys.exit(1)

    modified_count = inject_seed_to_prompts(experiment_dir, seed_path, verbose)

    if verbose:
        print()
        print("=" * 60)
        print(f"COMPLETE: {modified_count} system prompts modified")
        print("=" * 60)
        print()
        print("Next steps:")
        print(f"  1. Run experiments: python scripts/run_experiments.py --config {config_path}")
        print(f"  2. Classify results: python scripts/classify_results.py --results-dir results/{experiment_id}")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
