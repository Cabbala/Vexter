import json
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_paths_exist() -> None:
    required_paths = [
        "README.md",
        "docs/ROLE_DEFINITION.md",
        "docs/evaluation_contract.md",
        "docs/normalized_event_schema.md",
        "docs/metrics_catalog.md",
        "docs/comparison_matrix_template.md",
        "docs/comparison_collection_runbook.md",
        "docs/dexter_source_assessment.md",
        "docs/dexter_event_mapping.md",
        "docs/mewx_source_assessment.md",
        "docs/mewx_event_mapping.md",
        "specs/FIXED_WORKFLOW.md",
        "specs/ANALYSIS_CONTRACT.md",
        "ops/CODEX_MEMORY.md",
        "plans/IMPLEMENTATION_PLAN.md",
        "plans/TASK_000_BOOTSTRAP.md",
        "plans/SOURCE_ASSESSMENT_DEXTER.md",
        "plans/SOURCE_ASSESSMENT_MEWX.md",
        "plans/dexter_instrumentation_plan.md",
        "plans/mewx_instrumentation_plan.md",
        "plans/integration_readiness_plan.md",
        "manifests/reference_repos.json",
        "manifests/windows_runtime.json",
        "scripts/bootstrap_windows_workspace.sh",
        "scripts/sync_reference_repos.sh",
        "scripts/build_proof_bundle.sh",
        "scripts/comparison_analysis.py",
        "scripts/collect_comparison_package.ps1",
        "vexter/__init__.py",
        "vexter/comparison/__init__.py",
        "vexter/comparison/constants.py",
        "vexter/comparison/packages.py",
        "vexter/comparison/validator.py",
        "vexter/comparison/metrics.py",
        "vexter/comparison/pack.py",
        "tests/conftest.py",
        "artifacts/context_pack.json",
        "artifacts/summary.md",
        "artifacts/proof_bundle_manifest.json",
        "artifacts/task_ledger.jsonl",
        "artifacts/reports/task-005-live-collection-blocker.md",
        "artifacts/proofs/task-005-live-collection-check.json",
        "artifacts/examples/task-004-sample-comparison/pack_manifest.json",
        ".github/workflows/validate.yml",
    ]

    for relative_path in required_paths:
        assert (REPO_ROOT / relative_path).exists(), relative_path


def test_json_manifests_are_valid() -> None:
    json_paths = [
        REPO_ROOT / "manifests/reference_repos.json",
        REPO_ROOT / "manifests/windows_runtime.json",
        REPO_ROOT / "artifacts/context_pack.json",
        REPO_ROOT / "artifacts/proof_bundle_manifest.json",
    ]

    for path in json_paths:
        with path.open() as handle:
            payload = json.load(handle)
        assert payload


def test_reference_repo_manifest_has_expected_repos() -> None:
    with (REPO_ROOT / "manifests/reference_repos.json").open() as handle:
        manifest = json.load(handle)

    repo_names = {repo["name"] for repo in manifest["repos"]}
    assert repo_names == {"Dexter", "Mew-X"}


def test_windows_runtime_manifest_has_expected_shape() -> None:
    with (REPO_ROOT / "manifests/windows_runtime.json").open() as handle:
        manifest = json.load(handle)

    assert manifest["host_alias"] == "win-lan"
    assert manifest["selected_root"].endswith("Vexter")
    assert len(manifest["directories"]) == 8
    assert manifest["analysis_layout"]["dexter"]["raw_events"].endswith("data\\raw\\dexter")
    assert manifest["analysis_layout"]["mewx"]["raw_events"].endswith("data\\raw\\mewx")


def test_task_ledger_is_valid_jsonl() -> None:
    ledger_path = REPO_ROOT / "artifacts/task_ledger.jsonl"
    lines = ledger_path.read_text().strip().splitlines()

    assert len(lines) >= 3
    payload = json.loads(lines[-1])
    assert payload["task_id"] == "TASK-005-live-comparison-evidence"
    assert payload["status"] == "blocked_on_collection"
    assert payload["branch"] == "codex/task-005-live-comparison-evidence"
    assert payload["next_task_id"] == "BLOCKED"


def test_proof_bundle_exists_and_contains_required_files() -> None:
    with (REPO_ROOT / "artifacts/proof_bundle_manifest.json").open() as handle:
        manifest = json.load(handle)

    assert manifest["status"] == "blocked_on_collection"
    assert manifest["next_task"]["id"] == "BLOCKED"

    bundle_path = REPO_ROOT / manifest["bundle_path"]
    assert bundle_path.exists()

    with tarfile.open(bundle_path, "r:gz") as bundle:
        names = set(bundle.getnames())

    assert "README.md" in names
    assert "docs/evaluation_contract.md" in names
    assert "docs/normalized_event_schema.md" in names
    assert "docs/comparison_collection_runbook.md" in names
    assert "docs/dexter_event_mapping.md" in names
    assert "docs/mewx_event_mapping.md" in names
    assert "scripts/comparison_analysis.py" in names
    assert "scripts/collect_comparison_package.ps1" in names
    assert "vexter/comparison/validator.py" in names
    assert "artifacts/examples/task-004-sample-comparison/summary.md" in names
    assert "artifacts/reports/task-005-live-collection-blocker.md" in names
    assert "artifacts/proofs/task-005-live-collection-check.json" in names
    assert "artifacts/context_pack.json" in names
    assert "artifacts/proof_bundle_manifest.json" in names
    assert "tests/__pycache__/" not in names
