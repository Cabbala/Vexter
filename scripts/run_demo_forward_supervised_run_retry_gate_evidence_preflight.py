#!/usr/bin/env python3
"""Write the canonical retry-gate evidence preflight / reopen-readiness surfaces."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vexter.demo_readiness.external_evidence import write_external_evidence_artifacts
from vexter.planner_router.transport import DexterDemoRuntimeConfig

from scripts.run_demo_forward_supervised_run_retry_readiness import (
    parse_template_env,
    patched_demo_env,
)


TEMPLATE_ENV_PATH = ROOT / "templates" / "windows_runtime" / "dexter.env.example"


def main() -> None:
    template_env = parse_template_env(TEMPLATE_ENV_PATH)
    with patched_demo_env(template_env):
        runtime_config = DexterDemoRuntimeConfig.from_env()
    payloads = write_external_evidence_artifacts(ROOT, template_env, runtime_config)
    preflight = payloads["preflight"]
    readiness = preflight["reopen_readiness"]
    print(
        json.dumps(
            {
                "preflight_status": readiness["status"],
                "manifest_status": readiness["manifest_status"],
                "blocked_faces": readiness["blocked_faces"],
                "blocked_reason_counts": readiness["blocked_reason_counts"],
                "retry_gate_review_reopen_ready": readiness[
                    "retry_gate_review_reopen_ready"
                ],
                "canonical_command": readiness["canonical_command"],
            },
            indent=2,
            sort_keys=False,
        )
    )


if __name__ == "__main__":
    main()
