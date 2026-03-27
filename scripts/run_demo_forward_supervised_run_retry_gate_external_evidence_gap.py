#!/usr/bin/env python3
"""Write the canonical retry-gate external-evidence gap surfaces."""

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
    payload = payloads["gap"]
    preflight = payloads["preflight"]
    print(
        json.dumps(
            {
                "manifest_status": payload["manifest"]["status"],
                "preflight_status": preflight["reopen_readiness"]["status"],
                "blocked_faces": payload["summary"]["blocked_faces"],
                "blocked_reason_counts": preflight["reopen_readiness"]["blocked_reason_counts"],
                "retry_gate_review_reopen_ready": payload["summary"][
                    "retry_gate_review_reopen_ready"
                ],
                "template_only_false_path": preflight["reopen_readiness"]["template_only_false_path"],
                "consistency_checks": preflight["reopen_readiness"]["consistency_checks"],
                "next_human_pass": preflight["reopen_readiness"]["next_human_pass"],
            },
            indent=2,
            sort_keys=False,
        )
    )


if __name__ == "__main__":
    main()
