"""Demo-readiness helpers."""

from .external_evidence import (
    CONTRACT_SPEC_REL_PATH,
    GAP_PROOF_REL_PATH,
    GAP_REPORT_REL_PATH,
    GAP_SUMMARY_REL_PATH,
    MANIFEST_KIND,
    MANIFEST_REL_PATH,
    TASK_ID,
    render_gap_report_markdown,
    render_gap_summary_markdown,
    validate_external_evidence_manifest,
    write_external_evidence_gap_artifacts,
)

__all__ = [
    "CONTRACT_SPEC_REL_PATH",
    "GAP_PROOF_REL_PATH",
    "GAP_REPORT_REL_PATH",
    "GAP_SUMMARY_REL_PATH",
    "MANIFEST_KIND",
    "MANIFEST_REL_PATH",
    "TASK_ID",
    "render_gap_report_markdown",
    "render_gap_summary_markdown",
    "validate_external_evidence_manifest",
    "write_external_evidence_gap_artifacts",
]
