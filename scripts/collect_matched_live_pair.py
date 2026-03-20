#!/usr/bin/env python3
"""Collect a matched Dexter/Mew-X live pair from win-lan and copy packages locally."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WINDOWS_ROOT = r"C:\Users\bot\quant\Vexter"
DEFAULT_WINDOWS_HOST = "win-lan"
DEFAULT_MEWX_MODE = "sim"
DEFAULT_DURATION_SECONDS = 120
DEFAULT_GRACE_SECONDS = 20
DEFAULT_STARTUP_DELAY_SECONDS = 2


def iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def utc_stamp() -> str:
    return iso_utc(datetime.now(timezone.utc)).replace("-", "").replace(":", "")


def _run(
    args: list[str],
    *,
    cwd: Path | None = None,
    input_text: str | None = None,
    capture_output: bool = True,
) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            args,
            cwd=str(cwd) if cwd else None,
            input=input_text,
            text=True,
            capture_output=capture_output,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else ""
        stdout = exc.stdout.strip() if exc.stdout else ""
        detail = "\n".join(part for part in [stdout, stderr] if part)
        if detail:
            raise RuntimeError(f"command failed: {' '.join(args)}\n{detail}") from exc
        raise


def ssh(host: str, args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return _run(["ssh", host, *args], cwd=REPO_ROOT, input_text=input_text)


def scp_to(host: str, local_path: Path, remote_path: str) -> None:
    _run(["scp", str(local_path), f"{host}:{remote_path}"], cwd=REPO_ROOT, capture_output=True)


def scp_from(host: str, remote_path: str, local_dir: Path) -> None:
    local_dir.mkdir(parents=True, exist_ok=True)
    _run(["scp", "-r", f"{host}:{remote_path}", str(local_dir)], cwd=REPO_ROOT, capture_output=True)


def windows_to_scp_path(path: str) -> str:
    drive, remainder = path.split(":", 1)
    normalized = remainder.replace("\\", "/").lstrip("/")
    return f"/{drive.upper()}:/{normalized}"


def load_frozen_source_commits() -> dict[str, str]:
    context_pack = json.loads((REPO_ROOT / "artifacts" / "context_pack.json").read_text())
    return context_pack["current_task"]["frozen_source_commits"]


def build_remote_runner(config: dict[str, Any]) -> str:
    payload = json.dumps(config, sort_keys=True)
    return textwrap.dedent(
        f"""
        import collections
        import datetime as dt
        import json
        import os
        import pathlib
        import signal
        import subprocess
        import sys
        import time

        config = json.loads({payload!r})

        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, signal.SIG_IGN)
        if hasattr(signal, "SIGINT"):
            signal.signal(signal.SIGINT, signal.SIG_IGN)

        def iso_utc(value):
            return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")

        def event_summary(path_str):
            path = pathlib.Path(path_str)
            summary = {{
                "path": str(path),
                "exists": path.exists(),
                "event_count": 0,
                "first_ts_utc": None,
                "last_ts_utc": None,
                "event_types": {{}},
                "modes": [],
                "transport_modes": [],
            }}
            if not path.exists():
                return summary

            event_types = collections.Counter()
            modes = set()
            transport_modes = set()
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    event = json.loads(line)
                    ts_utc = event.get("ts_utc")
                    if ts_utc:
                        if summary["first_ts_utc"] is None:
                            summary["first_ts_utc"] = ts_utc
                        summary["last_ts_utc"] = ts_utc
                    event_type = event.get("event_type")
                    if event_type:
                        event_types[str(event_type)] += 1
                    mode = event.get("mode")
                    if mode:
                        modes.add(str(mode))
                    transport = event.get("transport_mode")
                    if transport:
                        transport_modes.add(str(transport))
                    summary["event_count"] += 1

            summary["event_types"] = dict(event_types)
            summary["modes"] = sorted(modes)
            summary["transport_modes"] = sorted(transport_modes)
            return summary

        def open_log(path_str):
            path = pathlib.Path(path_str)
            path.parent.mkdir(parents=True, exist_ok=True)
            return path.open("wb")

        windows_root = pathlib.Path(config["windows_root"])
        dexter_root = windows_root / "sources" / "Dexter"
        mewx_root = windows_root / "sources" / "Mew-X"
        logs_root = windows_root / "data" / "logs" / "unified" / "matched_pair_runner"
        logs_root.mkdir(parents=True, exist_ok=True)

        dexter_run_id = config["dexter_run_id"]
        mewx_run_id = config["mewx_run_id"]
        duration_seconds = int(config["duration_seconds"])
        grace_seconds = int(config["grace_seconds"])
        startup_delay_seconds = int(config["startup_delay_seconds"])

        common_env = {{
            "VEXTER_RUNTIME_ROOT": config["windows_root"],
            "VEXTER_OUTPUT_ROOT": config["windows_root"],
        }}

        dexter_env = os.environ.copy()
        dexter_env.update(common_env)
        dexter_env.update(
            {{
                "VEXTER_RUN_ID": dexter_run_id,
                "VEXTER_MODE": "observe_live",
                "VEXTER_TRANSPORT_MODE": "ws",
            }}
        )

        mewx_env = os.environ.copy()
        mewx_env.update(common_env)
        mewx_env.update(
            {{
                "VEXTER_RUN_ID": mewx_run_id,
                "MODE": config["mewx_mode"],
            }}
        )

        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        processes = []
        log_handles = []
        launch_events = []

        def start_process(name, cmd, cwd, env):
            stdout_handle = open_log(str(logs_root / f"{{name}}-{{config['label']}}.stdout.log"))
            stderr_handle = open_log(str(logs_root / f"{{name}}-{{config['label']}}.stderr.log"))
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                env=env,
                stdout=stdout_handle,
                stderr=stderr_handle,
                creationflags=creationflags,
            )
            processes.append((name, proc))
            log_handles.extend([stdout_handle, stderr_handle])
            launch_events.append(
                {{
                    "name": name,
                    "pid": proc.pid,
                    "launched_at_utc": iso_utc(dt.datetime.now(dt.timezone.utc)),
                    "cwd": str(cwd),
                    "cmd": cmd,
                }}
            )
            return proc

        measurement_started_at = None
        measurement_ended_at = None

        try:
            start_process(
                "dexter_wslogs",
                [config["dexter_python"], "DexLab/wsLogs.py"],
                dexter_root,
                dexter_env,
            )
            if startup_delay_seconds > 0:
                time.sleep(startup_delay_seconds)

            start_process(
                "dexter",
                [config["dexter_python"], "Dexter.py"],
                dexter_root,
                dexter_env,
            )
            start_process(
                "mewx",
                ["cargo", "run", "--quiet"],
                mewx_root,
                mewx_env,
            )

            measurement_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
            time.sleep(duration_seconds)
            measurement_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))

            for name, proc in reversed(processes):
                if proc.poll() is not None:
                    continue
                try:
                    proc.send_signal(signal.CTRL_BREAK_EVENT)
                except Exception:
                    pass

            deadline = time.time() + grace_seconds
            for _, proc in processes:
                remaining = max(0.0, deadline - time.time())
                try:
                    proc.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    proc.kill()
        finally:
            results = []
            for name, proc in processes:
                exit_code = proc.poll()
                if exit_code is None:
                    proc.kill()
                    exit_code = proc.wait(timeout=5)
                results.append({{"name": name, "pid": proc.pid, "exit_code": exit_code}})

            for handle in log_handles:
                handle.close()

            payload = {{
                "label": config["label"],
                "host": os.environ.get("COMPUTERNAME"),
                "measurement_window": {{
                    "started_at_utc": measurement_started_at,
                    "ended_at_utc": measurement_ended_at,
                }},
                "launch_events": launch_events,
                "process_results": results,
                "runs": {{
                    "dexter": {{
                        "run_id": dexter_run_id,
                        "event_summary": event_summary(str(windows_root / "data" / "raw" / "dexter" / f"{{dexter_run_id}}.ndjson")),
                    }},
                    "mewx": {{
                        "run_id": mewx_run_id,
                        "event_summary": event_summary(str(windows_root / "data" / "raw" / "mewx" / f"{{mewx_run_id}}.ndjson")),
                    }},
                }},
                "log_root": str(logs_root),
            }}
            print(json.dumps(payload))
        """
    ).strip()


def collect_remote_runs(
    *,
    host: str,
    windows_root: str,
    label: str,
    dexter_run_id: str,
    mewx_run_id: str,
    mewx_mode: str,
    duration_seconds: int,
    grace_seconds: int,
    startup_delay_seconds: int,
    dexter_python: str,
) -> dict[str, Any]:
    script = build_remote_runner(
        {
            "windows_root": windows_root,
            "label": label,
            "dexter_run_id": dexter_run_id,
            "mewx_run_id": mewx_run_id,
            "mewx_mode": mewx_mode,
            "duration_seconds": duration_seconds,
            "grace_seconds": grace_seconds,
            "startup_delay_seconds": startup_delay_seconds,
            "dexter_python": dexter_python,
        }
    )
    result = ssh(host, ["python", "-"], input_text=script)
    stdout = result.stdout.strip().splitlines()
    if not stdout:
        raise RuntimeError("remote collection returned no JSON payload")
    return json.loads(stdout[-1])


def ensure_remote_collector(host: str, windows_root: str) -> str:
    remote_tools_dir = f"{windows_root}\\tools"
    ssh(
        host,
        [
            "powershell",
            "-NoProfile",
            "-Command",
            f"New-Item -ItemType Directory -Force '{remote_tools_dir}' | Out-Null",
        ],
    )
    remote_collector = f"{remote_tools_dir}\\collect_comparison_package.ps1"
    scp_to(host, REPO_ROOT / "scripts" / "collect_comparison_package.ps1", windows_to_scp_path(remote_collector))
    return remote_collector


def package_remote_run(
    *,
    host: str,
    collector_path: str,
    source: str,
    run_id: str,
    source_commit: str,
    mode: str,
    transport_mode: str,
    started_at_utc: str,
    ended_at_utc: str,
    event_file: str,
    windows_root: str,
) -> str:
    result = ssh(
        host,
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            collector_path,
            "-Source",
            source,
            "-RunId",
            run_id,
            "-SourceCommit",
            source_commit,
            "-Mode",
            mode,
            "-TransportMode",
            transport_mode,
            "-StartedAtUtc",
            started_at_utc,
            "-EndedAtUtc",
            ended_at_utc,
            "-EventFile",
            event_file,
            "-RuntimeRoot",
            windows_root,
        ],
    )
    output = result.stdout.strip().splitlines()
    if not output:
        raise RuntimeError(f"collector did not return a package path for {source}")
    return output[-1].strip()


def local_stage_dir(label: str) -> Path:
    return REPO_ROOT / "artifacts" / "tmp" / f"winlan-packages-{label}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windows-host", default=DEFAULT_WINDOWS_HOST)
    parser.add_argument("--windows-root", default=DEFAULT_WINDOWS_ROOT)
    parser.add_argument("--duration-seconds", type=int, default=DEFAULT_DURATION_SECONDS)
    parser.add_argument("--grace-seconds", type=int, default=DEFAULT_GRACE_SECONDS)
    parser.add_argument("--startup-delay-seconds", type=int, default=DEFAULT_STARTUP_DELAY_SECONDS)
    parser.add_argument("--mewx-mode", choices=["sim", "trade"], default=DEFAULT_MEWX_MODE)
    parser.add_argument("--label")
    parser.add_argument("--output-json")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    label = args.label or f"pass-grade-attempt-{utc_stamp()}"
    commits = load_frozen_source_commits()

    dexter_run_id = f"dexter-{label}"
    mewx_run_id = f"mewx-{label}"
    collection = collect_remote_runs(
        host=args.windows_host,
        windows_root=args.windows_root,
        label=label,
        dexter_run_id=dexter_run_id,
        mewx_run_id=mewx_run_id,
        mewx_mode=args.mewx_mode,
        duration_seconds=args.duration_seconds,
        grace_seconds=args.grace_seconds,
        startup_delay_seconds=args.startup_delay_seconds,
        dexter_python=rf"{args.windows_root}\venvs\dexter\Scripts\python.exe",
    )

    measurement_window = collection["measurement_window"]
    started_at_utc = measurement_window["started_at_utc"]
    ended_at_utc = measurement_window["ended_at_utc"]
    if not started_at_utc or not ended_at_utc:
        raise RuntimeError("remote collection did not return a usable measurement window")

    dexter_summary = collection["runs"]["dexter"]["event_summary"]
    mewx_summary = collection["runs"]["mewx"]["event_summary"]
    if dexter_summary["event_count"] == 0 or mewx_summary["event_count"] == 0:
        raise RuntimeError(
            "matched pair collection produced an empty raw stream for at least one source"
        )

    collector_path = ensure_remote_collector(args.windows_host, args.windows_root)
    dexter_mode = dexter_summary["modes"][0] if dexter_summary["modes"] else "observe_live"
    dexter_transport = (
        dexter_summary["transport_modes"][0] if dexter_summary["transport_modes"] else "ws"
    )
    mewx_mode = mewx_summary["modes"][0] if mewx_summary["modes"] else (
        "sim_live" if args.mewx_mode == "sim" else "trade_live"
    )
    mewx_transport = mewx_summary["transport_modes"][0] if mewx_summary["transport_modes"] else "mixed"

    dexter_package_remote = package_remote_run(
        host=args.windows_host,
        collector_path=collector_path,
        source="dexter",
        run_id=dexter_run_id,
        source_commit=commits["dexter"],
        mode=dexter_mode,
        transport_mode=dexter_transport,
        started_at_utc=started_at_utc,
        ended_at_utc=ended_at_utc,
        event_file=dexter_summary["path"],
        windows_root=args.windows_root,
    )
    mewx_package_remote = package_remote_run(
        host=args.windows_host,
        collector_path=collector_path,
        source="mewx",
        run_id=mewx_run_id,
        source_commit=commits["mewx"],
        mode=mewx_mode,
        transport_mode=mewx_transport,
        started_at_utc=started_at_utc,
        ended_at_utc=ended_at_utc,
        event_file=mewx_summary["path"],
        windows_root=args.windows_root,
    )

    stage_dir = local_stage_dir(label)
    scp_from(args.windows_host, windows_to_scp_path(dexter_package_remote), stage_dir)
    scp_from(args.windows_host, windows_to_scp_path(mewx_package_remote), stage_dir)

    payload = {
        "label": label,
        "windows_host": args.windows_host,
        "windows_root": args.windows_root,
        "measurement_window": measurement_window,
        "remote_collection": collection,
        "remote_packages": {
            "dexter": dexter_package_remote,
            "mewx": mewx_package_remote,
        },
        "local_packages": {
            "dexter": str((stage_dir / dexter_run_id).resolve()),
            "mewx": str((stage_dir / mewx_run_id).resolve()),
        },
    }

    output_json = Path(args.output_json) if args.output_json else stage_dir / "collection-summary.json"
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
