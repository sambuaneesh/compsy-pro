from __future__ import annotations

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Placeholder for optional MLM PLL scoring.")
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    raise SystemExit(
        f"MLM PLL is optional/secondary and not implemented in primary pilot pipeline. config={args.config}"
    )


if __name__ == "__main__":
    main()
