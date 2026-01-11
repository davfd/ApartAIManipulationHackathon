#!/usr/bin/env python3
"""
V3 Capability Evaluation Runner - Dynamic SEED

Tests ACTUAL ACCURACY on capability evaluations using v3's mechanical classifier.
NO evaluation flags - questions route mechanically through safety sieve + operations gate.

Usage:
    python -X utf8 run_all_dynamic.py --model "google/gemini-2.5-flash" --full --workers 10
    python -X utf8 run_all_dynamic.py --limit 10              # Quick test
    python -X utf8 run_all_dynamic.py --subset --workers 10   # 1000 MMLU + full GSM8K/GPQA
"""

import os
import sys
import json
import time
import argparse
import threading
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add paths
sys.path.insert(0, str(Path(__file__).parent / 'capability_evaluations'))
sys.path.insert(0, str(Path(__file__).parent / 'capability_evaluations' / 'dynamic_seed'))

# V3 imports
import dynamic_seed.loader as seed_loader
from loaders import load_mmlu, load_gpqa, load_gsm8k
from prompts import build_capability_prompt
from extractors import extract_and_check

get_dynamic_seed_with_audit = seed_loader.get_dynamic_seed_with_audit

# Import API infrastructure (OpenRouter)
from api_providers import call_full_response, get_model, set_model

# Model configuration
MODEL_NAME = None

# Thread-safe progress
_progress_lock = threading.Lock()
_progress_count = 0
_progress_total = 0
_correct_count = 0
_tier_counts = {}

def _reset_progress(total: int):
    global _progress_count, _progress_total, _correct_count, _tier_counts
    with _progress_lock:
        _progress_count = 0
        _progress_total = total
        _correct_count = 0
        _tier_counts = {}

def _increment_progress(is_correct: bool, question_id: str, from_cache: bool, tier: str):
    global _progress_count, _correct_count, _tier_counts
    with _progress_lock:
        _progress_count += 1
        if is_correct:
            _correct_count += 1
        _tier_counts[tier] = _tier_counts.get(tier, 0) + 1
        cache_str = "(cached)" if from_cache else ""
        status = "CORRECT" if is_correct else "WRONG"
        if _progress_count % 50 == 0 or _progress_count <= 10:
            print(f"  [{_progress_count}/{_progress_total}] {tier} {question_id} -> {status} {cache_str}")


def sanitize_model_name(model: str) -> str:
    """Convert model name to safe folder name"""
    return model.replace("/", "_").replace(":", "_").replace(".", "_")

def get_results_path(evaluation: str, model: str) -> Path:
    """Get path for results directory."""
    model_folder = sanitize_model_name(model)
    base = Path("results_v3") / "capability_dynamic" / model_folder / "dynamic" / evaluation
    base.mkdir(parents=True, exist_ok=True)
    return base

def load_cached_result(question_id: str, evaluation: str, model: str) -> Optional[Dict]:
    """Load cached result if exists."""
    result_path = get_results_path(evaluation, model) / f"{question_id}.json"
    if result_path.exists():
        with open(result_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_result(result: Dict, question_id: str, evaluation: str, model: str):
    """Save result to JSON file."""
    result_path = get_results_path(evaluation, model) / f"{question_id}.json"
    with open(result_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def test_single_question(question: Dict, evaluation: str, model: str) -> Dict:
    """
    Test a single question with v3's dynamic SEED system.

    Returns result dict with tier, seed_length, correctness, etc.
    """
    question_id = question['id']

    # Check cache
    cached = load_cached_result(question_id, evaluation, model)
    if cached:
        # Handle both old and new field names
        is_correct = cached.get('is_correct', cached.get('correct', False))
        _increment_progress(is_correct, question_id, True, cached.get('tier', 0))
        return cached

    # Get dynamic SEED using v3's classifier (NO evaluation flag)
    seed_info = get_dynamic_seed_with_audit(question['question'])
    tier = seed_info['tier']
    seed_content = seed_info['seed']
    seed_length = len(seed_content)

    # Build prompt with SEED
    prompt = build_capability_prompt(question, evaluation, seed_content)

    # Call model via OpenRouter
    max_tokens = 500 if evaluation == "gsm8k" else 100
    response = call_full_response(prompt, max_tokens=max_tokens)

    # Check if API call succeeded
    if not response.get("success"):
        result = {
            'question_id': question_id,
            'evaluation': evaluation,
            'condition': 'dynamic',
            'model': model,
            'tier': tier,
            'seed_length': seed_length,
            'error': response.get('error', 'Unknown error'),
            'is_correct': False,
            'timestamp': datetime.now().isoformat(),
        }
        save_result(result, question_id, evaluation, model)
        _increment_progress(False, question_id, False, tier)
        return result

    # Extract response text
    model_response = response["content"]

    # Extract answer and check correctness
    extraction = extract_and_check(model_response, question, evaluation)

    # Build result
    result = {
        'question_id': question_id,
        'evaluation': evaluation,
        'condition': 'dynamic',
        'model': model,
        'tier': tier,
        'seed_length': seed_length,
        'question': question['question'][:200],
        'response': model_response,
        **extraction,
        'timestamp': datetime.now().isoformat(),
    }

    # Save result
    save_result(result, question_id, evaluation, model)

    # Update progress
    _increment_progress(result['is_correct'], question_id, False, tier)

    return result

def run_evaluation(evaluation_name: str, questions: List[Dict], model: str, workers: int = 10) -> Dict:
    """
    Run all questions in a evaluation using parallel execution.
    """
    print(f"\n{'='*70}")
    print(f"Running {evaluation_name.upper()} ({len(questions)} questions, {workers} workers)")
    print(f"{'='*70}\n")

    _reset_progress(len(questions))

    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(test_single_question, q, evaluation_name, model): q
            for q in questions
        }

        for future in as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"  ERROR: {e}")
                results.append({'is_correct': False, 'tier': 'ERROR'})

    # Final statistics
    accuracy = sum(r.get('is_correct', False) for r in results) / len(results) if results else 0
    tier_counts = {}
    for r in results:
        tier = r.get('tier', 'UNKNOWN')
        tier_counts[tier] = tier_counts.get(tier, 0) + 1

    print(f"\n{evaluation_name.upper()} Results:")
    print(f"  Accuracy: {accuracy:.1%} ({sum(r.get('is_correct', False) for r in results)}/{len(results)})")
    print(f"  Tier distribution:")
    for tier in sorted(tier_counts.keys()):
        pct = tier_counts[tier] / len(results) * 100
        print(f"    {tier}: {tier_counts[tier]} ({pct:.1f}%)")

    # Save summary
    summary = {
        "evaluation": evaluation_name,
        "n_questions": len(questions),
        "correct": sum(r.get('is_correct', False) for r in results),
        "accuracy": accuracy,
        "tier_distribution": tier_counts,
        "workers": workers,
        "timestamp": datetime.now().isoformat()
    }
    summary_path = get_results_path(evaluation_name, model) / "summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    return summary

def main():
    global MODEL_NAME

    parser = argparse.ArgumentParser(description='V3 Capability Evaluation Runner (Dynamic SEED)')
    parser.add_argument('--limit', type=int, default=10,
                        help='Limit questions per evaluation (default: 10)')
    parser.add_argument('--full', action='store_true',
                        help='Run all questions (no limit)')
    parser.add_argument('--subset', action='store_true',
                        help='Subset mode: 1000 MMLU + full GSM8K/GPQA (~2.7K total)')
    parser.add_argument('--mmlu-limit', type=int, default=None,
                        help='Custom MMLU limit (GSM8K/GPQA run full)')
    parser.add_argument('--evaluation', type=str, nargs='+',
                        choices=['mmlu', 'gpqa', 'gsm8k'],
                        help='Specific evaluation(s) to run')
    parser.add_argument('--model', type=str, default="google/gemini-2.5-flash",
                        help='Model to use (default: google/gemini-2.5-flash)')
    parser.add_argument('--workers', type=int, default=10,
                        help='Number of parallel workers (default: 10)')
    args = parser.parse_args()

    # Set model
    MODEL_NAME = args.model
    set_model(MODEL_NAME)
    print("="*70)
    print("V3 CAPABILITY BENCHMARK RUNNER (Dynamic SEED)")
    print("="*70)
    print(f"Model: {MODEL_NAME}")
    print(f"Classifier: V3 Mechanical Gate (NO evaluation flags)")
    print("="*70)

    # Determine limits
    if args.full:
        mmlu_limit = None
        other_limit = None
        print("Mode: FULL (all 15,809 questions)")
    elif args.subset:
        mmlu_limit = 1000
        other_limit = None
        print("Mode: SUBSET (1000 MMLU + full GSM8K/GPQA = ~2,770 questions)")
    elif args.mmlu_limit:
        mmlu_limit = args.mmlu_limit
        other_limit = None
        print(f"Mode: CUSTOM ({mmlu_limit} MMLU + full GSM8K/GPQA)")
    else:
        mmlu_limit = args.limit
        other_limit = args.limit
        print(f"Mode: QUICK TEST ({args.limit} per evaluation)")

    # Load evaluations
    print("\nLoading evaluations...")
    evaluations = args.evaluation if args.evaluation else ["mmlu", "gpqa", "gsm8k"]

    evaluation_data = {}
    if "mmlu" in evaluations:
        evaluation_data["mmlu"] = load_mmlu(limit=mmlu_limit)
        print(f"[OK] Loaded {len(evaluation_data['mmlu'])} MMLU questions")
    if "gpqa" in evaluations:
        evaluation_data["gpqa"] = load_gpqa(limit=other_limit)
        print(f"[OK] Loaded {len(evaluation_data['gpqa'])} GPQA questions")
    if "gsm8k" in evaluations:
        evaluation_data["gsm8k"] = load_gsm8k(limit=other_limit)
        print(f"[OK] Loaded {len(evaluation_data['gsm8k'])} GSM8K questions")

    # Run evaluations
    results = {}
    for bench_name, questions in evaluation_data.items():
        summary = run_evaluation(bench_name, questions, MODEL_NAME, args.workers)
        results[bench_name] = summary

    # Overall statistics
    total_questions = sum(r['n_questions'] for r in results.values())
    total_correct = sum(r.get('correct', 0) for r in results.values())
    overall_accuracy = total_correct / total_questions if total_questions > 0 else 0

    print("\n" + "="*70)
    print("OVERALL RESULTS")
    print("="*70)
    print(f"Total questions: {total_questions}")
    print(f"Overall accuracy: {overall_accuracy:.1%} ({total_correct}/{total_questions})")
    print("="*70)
    print(f"\nResults saved to: results_v3/capability_dynamic/{sanitize_model_name(MODEL_NAME)}/")

    return 0

if __name__ == "__main__":
    sys.exit(main())
