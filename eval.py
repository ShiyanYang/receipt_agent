#!/usr/bin/env python3
"""
eval.py - evaluate the Agent by running multiple generations and producing simple metrics.
"""
import argparse
import json
import time
from pathlib import Path
from statistics import mean, median
from typing import Any, Callable, Dict, List
import multiprocessing as mp

from agent import Agent


def _callable_from_agent(agent: Agent, names: List[str]) -> Callable:
    for name in names:
        fn = getattr(agent, name, None)
        if callable(fn):
            return fn
    raise AttributeError(f"Agent has none of the methods: {names}")


def _estimate_length(obj: Any) -> int:
    if isinstance(obj, (list, tuple, set, dict)):
        return len(obj)
    if isinstance(obj, str):
        lines = [l for l in obj.splitlines() if l.strip()]
        if len(lines) > 1:
            return len(lines)
        parts = [p.strip() for p in obj.split(",") if p.strip()]
        return max(1, len(parts))
    return 1


def _normalize_shopping_list(obj: Any) -> List[str]:
    if obj is None:
        return []
    if isinstance(obj, (list, tuple)):
        return [str(x).strip() for x in obj if str(x).strip()]
    s = str(obj).strip()
    if not s:
        return []
    lines = [l.strip() for l in s.splitlines() if l.strip()]
    if len(lines) > 1:
        return lines
    parts = [p.strip() for p in s.split(",") if p.strip()]
    if parts:
        return parts
    parts = [p.strip() for p in s.split(";") if p.strip()]
    if parts:
        return parts
    return [s]


def _worker(model_path: str, q: mp.Queue) -> None:
    try:
        agent = Agent(model_path)
        meal_plan_fn = _callable_from_agent(agent, ["generate_meal_plan", "generateMealPlan"])
        shopping_fn = _callable_from_agent(agent, ["generate_shoppling_list", "generate_shopping_list", "generateShoppingList"])

        start_total = time.time()
        start_mp = time.time()
        mp_out = meal_plan_fn()
        meal_time = time.time() - start_mp

        start_sl = time.time()
        sl_out = shopping_fn(mp_out)
        shopping_time = time.time() - start_sl

        total_time = time.time() - start_total

        q.put({
            "meal_plan": mp_out,
            "shopping_list": sl_out,
            "meal_time": meal_time,
            "shopping_time": shopping_time,
            "total_time": total_time,
            "error": None,
        })
    except Exception as e:
        q.put({
            "meal_plan": None,
            "shopping_list": None,
            "meal_time": None,
            "shopping_time": None,
            "total_time": None,
            "error": str(e),
        })


def evaluate(model_path: str, iterations: int = 5, timeout: int = 60, output: str = "eval_results.json") -> Dict[str, Any]:
    runs = []
    times = []
    meal_plans = []
    shopping_lists = []
    timeouts = 0
    errors = 0

    for i in range(max(1, int(iterations))):
        q: mp.Queue = mp.Queue()
        p = mp.Process(target=_worker, args=(model_path, q))
        p.start()
        p.join(timeout)
        timed_out = False
        result: Dict[str, Any] = {}
        if p.is_alive():
            p.terminate()
            p.join()
            timed_out = True
            timeouts += 1
            result = {
                "meal_plan": None,
                "shopping_list": None,
                "meal_time": None,
                "shopping_time": None,
                "total_time": None,
                "error": "timeout",
            }
        else:
            try:
                result = q.get_nowait()
                if result.get("error"):
                    errors += 1
            except Exception:
                result = {
                    "meal_plan": None,
                    "shopping_list": None,
                    "meal_time": None,
                    "shopping_time": None,
                    "total_time": None,
                    "error": "no result",
                }
                errors += 1

        mp_out = result.get("meal_plan")
        sl_out = result.get("shopping_list")
        meal_time = result.get("meal_time")
        shopping_time = result.get("shopping_time")
        total_time = result.get("total_time")

        normalized_sl = _normalize_shopping_list(sl_out)
        is_ingredient_list = isinstance(normalized_sl, list) and len(normalized_sl) > 0 and all(isinstance(x, str) and 1 <= len(x) <= 120 for x in normalized_sl)

        runs.append({
            "iteration": i + 1,
            "timeout": timed_out,
            "error": result.get("error"),
            "meal_time": meal_time,
            "shopping_time": shopping_time,
            "total_time": total_time,
            "raw_meal_plan": mp_out if isinstance(mp_out, (str, list, dict)) else str(mp_out),
            "raw_shopping_list": sl_out if isinstance(sl_out, (str, list, dict)) else str(sl_out),
            "normalized_shopping_list": normalized_sl,
            "is_ingredient_list": is_ingredient_list,
            "shopping_list_length_est": _estimate_length(sl_out),
        })

        if total_time is not None:
            times.append(total_time)
        meal_plans.append(str(mp_out))
        shopping_lists.append(str(sl_out))

    def max_consecutive_identical(items: List[str]) -> int:
        maxc = 0
        cur = None
        cnt = 0
        for it in items:
            if it == cur:
                cnt += 1
            else:
                cur = it
                cnt = 1
            if cnt > maxc:
                maxc = cnt
        return maxc

    max_consec_meal = max_consecutive_identical(meal_plans)
    max_consec_shop = max_consecutive_identical(shopping_lists)
    possible_loop = (max_consec_meal >= 3) or (max_consec_shop >= 3) or (timeouts > 0)

    summary = {
        "model": Path(model_path).name,
        "iterations": len(runs),
        "timeouts": timeouts,
        "errors": errors,
        "stuck_or_possible_loop": possible_loop,
        "time_seconds": {
            "avg": mean(times) if times else 0.0,
            "median": median(times) if times else 0.0,
            "min": min(times) if times else 0.0,
            "max": max(times) if times else 0.0,
        },
        "meal_plans": {
            "unique_count": len({x for x in meal_plans}),
            "example": meal_plans[0] if meal_plans else None,
            "max_consecutive_identical": max_consec_meal,
        },
        "shopping_lists": {
            "unique_count": len({x for x in shopping_lists}),
            "avg_length_estimate": mean([_estimate_length(x) for x in shopping_lists]) if shopping_lists else 0,
            "example": shopping_lists[0] if shopping_lists else None,
            "max_consecutive_identical": max_consec_shop,
        },
    }

    results = {"summary": summary, "runs": runs}
    with open(output, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Saved evaluation to {output}")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return results


def _cli():
    p = argparse.ArgumentParser(description="Evaluate Agent generation behavior.")
    p.add_argument("--model", "-m", default="./models/llama-3-8b-instruct.gguf", help="Path to model or agent config")
    p.add_argument("--iterations", "-n", type=int, default=5, help="Number of runs to perform")
    p.add_argument("--timeout", "-t", type=int, default=60, help="Timeout (seconds) for each iteration/process")
    p.add_argument("--output", "-o", default="eval_results.json", help="Output JSON file for results")
    args = p.parse_args()
    evaluate(args.model, args.iterations, args.timeout, args.output)


if __name__ == "__main__":
    _cli()
# ...existing code...