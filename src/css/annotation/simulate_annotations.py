from __future__ import annotations

import argparse
import random

import pandas as pd


def _base_score(phenomenon: str) -> float:
    if phenomenon == "role_reversal":
        return 4.2
    if phenomenon == "negation":
        return 3.6
    if phenomenon == "attachment":
        return 2.8
    return 3.0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create synthetic pilot annotations (for pipeline testing only)."
    )
    parser.add_argument("--batch", required=True)
    parser.add_argument("--output", default="data/annotations/human_css_0_5.csv")
    parser.add_argument("--annotators", type=int, default=3)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args()

    rng = random.Random(args.seed)
    batch = pd.read_csv(args.batch)
    out = []
    for _, row in batch.iterrows():
        for ann_i in range(args.annotators):
            base = _base_score(str(row["phenomenon"]))
            score = min(5.0, max(0.0, base + rng.uniform(-0.8, 0.8)))
            out.append(
                {
                    "pair_id": row["pair_id"],
                    "phenomenon": row["phenomenon"],
                    "s": row["s"],
                    "s_cf": row["s_cf"],
                    "annotator_id": f"sim_{ann_i + 1}",
                    "batch_id": "pilot_simulated_v1",
                    "human_change_0_5": round(score, 2),
                    "confidence_1_5": round(min(5.0, max(1.0, 4.0 + rng.uniform(-1.2, 0.8))), 2),
                    "fluency_s_1_5": 5.0,
                    "fluency_cf_1_5": 5.0,
                    "plausibility_s_1_5": round(
                        min(5.0, max(1.0, 4.2 + rng.uniform(-1.0, 0.6))), 2
                    ),
                    "plausibility_cf_1_5": round(
                        min(5.0, max(1.0, 4.0 + rng.uniform(-1.0, 0.6))), 2
                    ),
                    "changed_words": "",
                    "attention_check": True,
                    "created_at": "simulated",
                }
            )

    pd.DataFrame(out).to_csv(args.output, index=False)
    print(f"wrote {args.output} rows={len(out)} (SIMULATED)")


if __name__ == "__main__":
    main()
