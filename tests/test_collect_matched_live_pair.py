import importlib.util
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "collect_matched_live_pair.py"


def load_module():
    spec = importlib.util.spec_from_file_location("collect_matched_live_pair", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parser_defaults_include_rate_limit_mitigation_knobs() -> None:
    module = load_module()

    args = module.build_parser().parse_args([])

    assert args.dexter_mode == module.DEFAULT_DEXTER_MODE
    assert args.dexter_retry_backoff_seconds == module.DEFAULT_DEXTER_RETRY_BACKOFF_SECONDS
    assert args.dexter_prestart_quiet_seconds == module.DEFAULT_DEXTER_PRESTART_QUIET_SECONDS
    assert (
        args.dexter_wslogs_ready_timeout_seconds
        == module.DEFAULT_DEXTER_WSLOGS_READY_TIMEOUT_SECONDS
    )
    assert args.dexter_wslogs_settle_seconds == module.DEFAULT_DEXTER_WSLOGS_SETTLE_SECONDS


def test_run_uses_utf8_replace_for_remote_windows_output(monkeypatch) -> None:
    module = load_module()
    recorded: dict[str, object] = {}

    def fake_run(*args, **kwargs):
        recorded.update(kwargs)
        return subprocess.CompletedProcess(args=args[0], returncode=0, stdout="", stderr="")

    monkeypatch.setattr(module.subprocess, "run", fake_run)

    module._run(["ssh", "win-lan", "cmd", "/c", "dir"])

    assert recorded["text"] is True
    assert recorded["encoding"] == "utf-8"
    assert recorded["errors"] == "replace"


def test_remote_runner_records_wslogs_and_retry_timing() -> None:
    module = load_module()

    script = module.build_remote_runner(
        {
            "windows_root": r"C:\Users\bot\quant\Vexter",
            "label": "fixture-label",
            "dexter_run_id": "dexter-fixture",
            "mewx_run_id": "mewx-fixture",
            "dexter_mode": "paper_live",
            "mewx_mode": "sim",
            "duration_seconds": 120,
            "grace_seconds": 20,
            "startup_delay_seconds": 5,
            "mewx_ready_timeout_seconds": 90,
            "dexter_ready_timeout_seconds": 30,
            "dexter_startup_attempts": 4,
            "dexter_retry_backoff_seconds": 90,
            "dexter_prestart_quiet_seconds": 60,
            "dexter_wslogs_ready_timeout_seconds": 90,
            "dexter_wslogs_settle_seconds": 20,
            "dexter_python": r"C:\Users\bot\quant\Vexter\venvs\dexter\Scripts\python.exe",
        }
    )

    assert "dexter_wslogs_readiness" in script
    assert "stale_process_cleanup" in script
    assert "retry_backoff_started_at_utc" in script
    assert "retry_backoff_ended_at_utc" in script
    assert "prestart_quiet_seconds" in script
    assert "start_after_dexter_head_start" in script
    assert "wslogs_started_during_attempt" in script
    assert "wallet_balance_http_429_count" in script
    assert '"VEXTER_MODE": config["dexter_mode"]' in script
