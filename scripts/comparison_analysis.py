#!/usr/bin/env python3
"""CLI for Vexter comparison-analysis workflows."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from vexter.comparison import build_comparison_pack, derive_metrics, validate_run_package


def _write_payload(payload: dict, output_path: str | None) -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w") as handle:
            json.dump(payload, handle, indent=2, sort_keys=True)
            handle.write("\n")
        print(target)
        return
    print(json.dumps(payload, indent=2, sort_keys=True))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate a comparison run package")
    validate_parser.add_argument("--package-dir", required=True)
    validate_parser.add_argument("--output")

    metrics_parser = subparsers.add_parser("derive-metrics", help="Derive critical metrics for one run package")
    metrics_parser.add_argument("--package-dir", required=True)
    metrics_parser.add_argument("--output")

    pack_parser = subparsers.add_parser("build-pack", help="Build the first side-by-side comparison pack")
    pack_parser.add_argument("--dexter-package", required=True)
    pack_parser.add_argument("--mewx-package", required=True)
    pack_parser.add_argument("--output-dir", required=True)
    pack_parser.add_argument("--summary-note")
    pack_parser.add_argument("--output")
    pack_parser.add_argument(
        "--defer-winners",
        action="store_true",
        help="Populate the matrix while keeping winner columns pending.",
    )

    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "validate":
        _write_payload(validate_run_package(args.package_dir), args.output)
        return 0

    if args.command == "derive-metrics":
        _write_payload(derive_metrics(args.package_dir), args.output)
        return 0

    if args.command == "build-pack":
        payload = build_comparison_pack(
            dexter_package_dir=args.dexter_package,
            mewx_package_dir=args.mewx_package,
            output_dir=args.output_dir,
            summary_note=args.summary_note,
            defer_winners=args.defer_winners,
        )
        print(Path(args.output_dir).resolve())
        if not args.output:
            return 0
        _write_payload(payload, args.output)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
