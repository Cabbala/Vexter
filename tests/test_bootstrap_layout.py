import json
import tarfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_required_paths_exist() -> None:
    required_paths = [
        "README.md",
        "docs/ROLE_DEFINITION.md",
        "specs/FIXED_WORKFLOW.md",
        "specs/ANALYSIS_CONTRACT.md",
        "ops/CODEX_MEMORY.md",
        "plans/IMPLEMENTATION_PLAN.md",
        "plans/TASK_000_BOOTSTRAP.md",
        "plans/SOURCE_ASSESSMENT_DEXTER.md",
        "plans/SOURCE_ASSESSMENT_MEWX.md",
        "manifests/reference_repos.json",
        "manifests/windows_runtime.json",
        "scripts/bootstrap_windows_workspace.sh",
        "scripts/sync_reference_repos.sh",
        "scripts/build_proof_bundle.sh",
        "artifacts/context_pack.json",
        "artifacts/summary.md",
        "artifacts/proof_bundle_manifest.json",
        "artifacts/task_ledger.jsonl",
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


def test_task_ledger_is_valid_jsonl() -> None:
    ledger_path = REPO_ROOT / "artifacts/task_ledger.jsonl"
    lines = ledger_path.read_text().strip().splitlines()

    assert len(lines) == 1
    payload = json.loads(lines[0])
    assert payload["task_id"] == "TASK-000-bootstrap"


def test_proof_bundle_exists_and_contains_required_files() -> None:
    bundle_path = REPO_ROOT / "artifacts/bundles/task-000-bootstrap.tar.gz"
    assert bundle_path.exists()

    with tarfile.open(bundle_path, "r:gz") as bundle:
        names = set(bundle.getnames())

    assert "README.md" in names
    assert "artifacts/context_pack.json" in names
    assert "artifacts/proof_bundle_manifest.json" in names
