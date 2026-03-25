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

from vexter.comparison import (
    build_comparison_pack,
    derive_metrics,
    run_replay_deepening,
    run_replay_validation,
    validate_run_package,
)


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


def _write_text(payload: str, output_path: str | None) -> None:
    if output_path:
        target = Path(output_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload)
        print(target)
        return
    print(payload)


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

    replay_parser = subparsers.add_parser(
        "replay-validation",
        help="Evaluate promoted and confirmatory packs for downstream replay validation",
    )
    replay_parser.add_argument("--promoted-dexter-package", required=True)
    replay_parser.add_argument("--promoted-mewx-package", required=True)
    replay_parser.add_argument("--promoted-output-dir", required=True)
    replay_parser.add_argument("--confirmatory-dexter-package", required=True)
    replay_parser.add_argument("--confirmatory-mewx-package", required=True)
    replay_parser.add_argument("--confirmatory-output-dir", required=True)
    replay_parser.add_argument("--promoted-summary-note")
    replay_parser.add_argument("--confirmatory-summary-note")
    replay_parser.add_argument("--output", required=True)
    replay_parser.add_argument("--summary-output")

    deepening_parser = subparsers.add_parser(
        "replay-deepening",
        help="Reconstruct replay-mode packages from a promoted live baseline and measure live-vs-replay gap",
    )
    deepening_parser.add_argument("--latest-vexter-pr", required=True, type=int)
    deepening_parser.add_argument("--latest-vexter-main-commit", required=True)
    deepening_parser.add_argument("--dexter-main-commit", required=True)
    deepening_parser.add_argument("--mewx-frozen-commit", required=True)
    deepening_parser.add_argument("--promoted-label", required=True)
    deepening_parser.add_argument("--promoted-dexter-package", required=True)
    deepening_parser.add_argument("--promoted-mewx-package", required=True)
    deepening_parser.add_argument("--replay-package-root", required=True)
    deepening_parser.add_argument("--replay-output-dir", required=True)
    deepening_parser.add_argument("--confirmatory-residual-note", required=True)
    deepening_parser.add_argument("--output", required=True)
    deepening_parser.add_argument("--summary-output")

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

    if args.command == "replay-validation":
        payload, summary = run_replay_validation(
            promoted_dexter_package_dir=args.promoted_dexter_package,
            promoted_mewx_package_dir=args.promoted_mewx_package,
            promoted_output_dir=args.promoted_output_dir,
            confirmatory_dexter_package_dir=args.confirmatory_dexter_package,
            confirmatory_mewx_package_dir=args.confirmatory_mewx_package,
            confirmatory_output_dir=args.confirmatory_output_dir,
            promoted_summary_note=args.promoted_summary_note,
            confirmatory_summary_note=args.confirmatory_summary_note,
        )
        _write_payload(payload, args.output)
        _write_text(summary, args.summary_output)
        return 0

    if args.command == "replay-deepening":
        payload, summary = run_replay_deepening(
            latest_vexter_pr=args.latest_vexter_pr,
            latest_vexter_main_commit=args.latest_vexter_main_commit,
            dexter_main_commit=args.dexter_main_commit,
            mewx_frozen_commit=args.mewx_frozen_commit,
            promoted_label=args.promoted_label,
            promoted_dexter_package_dir=args.promoted_dexter_package,
            promoted_mewx_package_dir=args.promoted_mewx_package,
            replay_package_root=args.replay_package_root,
            replay_output_dir=args.replay_output_dir,
            confirmatory_residual_note=args.confirmatory_residual_note,
        )
        _write_payload(payload, args.output)
        _write_text(summary, args.summary_output)
        return 0

    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
