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
DEFAULT_MEWX_READY_TIMEOUT_SECONDS = 90
DEFAULT_DEXTER_READY_TIMEOUT_SECONDS = 30
DEFAULT_DEXTER_STARTUP_ATTEMPTS = 3
DEFAULT_DEXTER_RETRY_BACKOFF_SECONDS = 45
DEFAULT_DEXTER_PRESTART_QUIET_SECONDS = 30
DEFAULT_DEXTER_WSLOGS_READY_TIMEOUT_SECONDS = 75
DEFAULT_DEXTER_WSLOGS_SETTLE_SECONDS = 15


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
            encoding="utf-8",
            errors="replace",
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
        dexter_event_path = windows_root / "data" / "raw" / "dexter" / f"{{config['dexter_run_id']}}.ndjson"
        mewx_event_path = windows_root / "data" / "raw" / "mewx" / f"{{config['mewx_run_id']}}.ndjson"

        dexter_run_id = config["dexter_run_id"]
        mewx_run_id = config["mewx_run_id"]
        duration_seconds = int(config["duration_seconds"])
        grace_seconds = int(config["grace_seconds"])
        startup_delay_seconds = int(config["startup_delay_seconds"])
        mewx_ready_timeout_seconds = int(config["mewx_ready_timeout_seconds"])
        dexter_ready_timeout_seconds = int(config["dexter_ready_timeout_seconds"])
        dexter_startup_attempts = int(config["dexter_startup_attempts"])
        dexter_retry_backoff_seconds = int(config["dexter_retry_backoff_seconds"])
        dexter_prestart_quiet_seconds = int(config["dexter_prestart_quiet_seconds"])
        dexter_wslogs_ready_timeout_seconds = int(config["dexter_wslogs_ready_timeout_seconds"])
        dexter_wslogs_settle_seconds = int(config["dexter_wslogs_settle_seconds"])

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
        process_map = {{}}
        log_handles = []
        launch_events = []

        def log_path(name, stream):
            return logs_root / f"{{name}}-{{config['label']}}.{{stream}}.log"

        def read_log(path_str):
            path = pathlib.Path(path_str)
            if not path.exists():
                return ""
            return path.read_text(encoding="utf-8", errors="ignore")

        def count_log_occurrences(path_str, needle):
            return read_log(path_str).count(needle)

        def tail_text_lines(text, max_lines=12):
            if not text:
                return []
            lines = [line for line in text.splitlines() if line.strip()]
            if len(lines) <= max_lines:
                return lines
            return lines[-max_lines:]

        def tail_log_lines(path_str, max_lines=12):
            return tail_text_lines(read_log(path_str), max_lines=max_lines)

        def normalize_process_records(payload_text):
            if not payload_text.strip():
                return []
            parsed = json.loads(payload_text)
            if isinstance(parsed, dict):
                parsed = [parsed]
            return [
                {{
                    "name": record.get("Name"),
                    "process_id": record.get("ProcessId"),
                    "creation_date": record.get("CreationDate"),
                    "command_line": record.get("CommandLine"),
                }}
                for record in parsed
            ]

        def cleanup_stale_processes():
            powershell_script = r'''
            $targets = Get-CimInstance Win32_Process | Where-Object {{
                $_.CommandLine -and (
                    $_.CommandLine -match 'Dexter\\.py' -or
                    $_.CommandLine -match 'DexLab\\\\wsLogs\\.py' -or
                    $_.CommandLine -match 'Mew-X\\\\target\\\\debug\\\\mew\\.exe' -or
                    ($_.Name -eq 'cargo.exe' -and $_.CommandLine -match 'Mew-X')
                )
            }}
            $targets | Select-Object Name,ProcessId,CreationDate,CommandLine | ConvertTo-Json -Compress
            '''
            listed_at = iso_utc(dt.datetime.now(dt.timezone.utc))
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", powershell_script],
                text=True,
                capture_output=True,
            )
            cleanup = {{
                "listed_at_utc": listed_at,
                "list_exit_code": result.returncode,
                "list_stderr_tail": tail_text_lines(result.stderr),
                "found": [],
                "stopped": [],
            }}
            if result.returncode != 0:
                return cleanup

            cleanup["found"] = normalize_process_records(result.stdout)
            for record in cleanup["found"]:
                process_id = record.get("process_id")
                if process_id is None:
                    continue
                stop_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                stop = subprocess.run(
                    ["taskkill", "/PID", str(process_id), "/T", "/F"],
                    text=True,
                    capture_output=True,
                )
                cleanup["stopped"].append(
                    {{
                        **record,
                        "stop_started_at_utc": stop_started_at,
                        "stop_finished_at_utc": iso_utc(dt.datetime.now(dt.timezone.utc)),
                        "stop_exit_code": stop.returncode,
                        "stop_stdout_tail": tail_text_lines(stop.stdout),
                        "stop_stderr_tail": tail_text_lines(stop.stderr),
                    }}
                )
            return cleanup

        def start_process(name, cmd, cwd, env, *, alias=None):
            stdout_path = log_path(name, "stdout")
            stderr_path = log_path(name, "stderr")
            stdout_handle = open_log(str(stdout_path))
            stderr_handle = open_log(str(stderr_path))
            proc = subprocess.Popen(
                cmd,
                cwd=str(cwd),
                env=env,
                stdout=stdout_handle,
                stderr=stderr_handle,
                creationflags=creationflags,
            )
            processes.append((name, proc))
            process_map[alias or name] = proc
            log_handles.extend([stdout_handle, stderr_handle])
            launch_events.append(
                {{
                    "name": name,
                    "pid": proc.pid,
                    "launched_at_utc": iso_utc(dt.datetime.now(dt.timezone.utc)),
                    "cwd": str(cwd),
                    "cmd": cmd,
                    "stdout_path": str(stdout_path),
                    "stderr_path": str(stderr_path),
                }}
            )
            return proc, str(stdout_path), str(stderr_path)

        def wait_for_event_or_exit(path_str, timeout_seconds, process_name):
            deadline = time.time() + max(0, timeout_seconds)
            while time.time() <= deadline:
                summary = event_summary(path_str)
                if summary["event_count"] > 0:
                    return summary, iso_utc(dt.datetime.now(dt.timezone.utc)), False
                proc = process_map.get(process_name)
                if proc is not None and proc.poll() is not None:
                    return summary, None, True
                time.sleep(1)
            return event_summary(path_str), None, False

        def wait_for_log_pattern(path_str, pattern, timeout_seconds, process_name):
            deadline = time.time() + max(0, timeout_seconds)
            while time.time() <= deadline:
                if pattern in read_log(path_str):
                    return iso_utc(dt.datetime.now(dt.timezone.utc)), False
                proc = process_map.get(process_name)
                if proc is not None and proc.poll() is not None:
                    return None, True
                time.sleep(1)
            return None, False

        def request_shutdown(name):
            proc = process_map.get(name)
            if proc is None or proc.poll() is not None:
                return
            try:
                proc.send_signal(signal.CTRL_BREAK_EVENT)
            except Exception:
                pass

        def start_dexter_with_retries():
            attempt_records = []
            for attempt in range(1, max(1, dexter_startup_attempts) + 1):
                process_name = "dexter" if attempt == 1 else f"dexter_retry_{{attempt}}"
                attempt_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                wslogs_started_before_attempt = bool(wslogs_state["started"])
                proc, _stdout_path, stderr_path = start_process(
                    process_name,
                    [config["dexter_python"], "Dexter.py"],
                    dexter_root,
                    dexter_env,
                    alias="dexter",
                )
                wslogs_started_during_attempt = False
                if not wslogs_state["started"] and startup_delay_seconds > 0 and proc.poll() is None:
                    time.sleep(startup_delay_seconds)
                if not wslogs_state["started"] and proc.poll() is None:
                    start_process(
                        "dexter_wslogs",
                        [config["dexter_python"], "DexLab/wsLogs.py"],
                        dexter_root,
                        dexter_env,
                    )
                    wslogs_state["started"] = True
                    wslogs_state["started_after_attempt"] = attempt
                    wslogs_started_during_attempt = True
                    (
                        wslogs_state["observed_at_utc"],
                        wslogs_state["process_exited_before_subscription"],
                    ) = wait_for_log_pattern(
                        wslogs_state["stderr_path"],
                        "Subscribed to logs successfully!",
                        dexter_wslogs_ready_timeout_seconds,
                        "dexter_wslogs",
                    )
                    if wslogs_state["observed_at_utc"] and dexter_wslogs_settle_seconds > 0:
                        wslogs_state["settle_started_at_utc"] = iso_utc(dt.datetime.now(dt.timezone.utc))
                        time.sleep(dexter_wslogs_settle_seconds)
                        wslogs_state["settle_ended_at_utc"] = iso_utc(dt.datetime.now(dt.timezone.utc))
                summary, observed_at, exited_before_ready = wait_for_event_or_exit(
                    str(dexter_event_path),
                    dexter_ready_timeout_seconds,
                    "dexter",
                )
                attempt_finished_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                record = {{
                    "attempt": attempt,
                    "started_at_utc": attempt_started_at,
                    "finished_at_utc": attempt_finished_at,
                    "event_observed": bool(observed_at),
                    "observed_at_utc": observed_at,
                    "process_exited_before_event": exited_before_ready,
                    "event_count": summary["event_count"],
                    "exit_code": proc.poll(),
                    "stderr_path": stderr_path,
                    "wslogs_started_before_attempt": wslogs_started_before_attempt,
                    "wslogs_started_during_attempt": wslogs_started_during_attempt,
                    "head_start_seconds_before_wslogs": startup_delay_seconds if wslogs_started_during_attempt else 0,
                    "wallet_balance_http_429_count": count_log_occurrences(stderr_path, 'HTTP 429'),
                    "wallet_balance_rate_limited": 'rate limited' in read_log(stderr_path),
                    "stderr_tail": tail_log_lines(stderr_path),
                }}
                if summary["event_count"] > 0 or not exited_before_ready or attempt >= dexter_startup_attempts:
                    attempt_records.append(record)
                    return summary, observed_at, exited_before_ready, attempt_records
                if dexter_retry_backoff_seconds > 0:
                    record["retry_backoff_started_at_utc"] = iso_utc(dt.datetime.now(dt.timezone.utc))
                    time.sleep(max(0, dexter_retry_backoff_seconds))
                    record["retry_backoff_ended_at_utc"] = iso_utc(dt.datetime.now(dt.timezone.utc))
                attempt_records.append(record)
            return event_summary(str(dexter_event_path)), None, True, attempt_records

        measurement_started_at = None
        measurement_ended_at = None
        mewx_ready_summary = None
        mewx_ready_at = None
        mewx_exited_before_ready = False
        dexter_ready_summary = None
        dexter_ready_at = None
        dexter_exited_before_ready = False
        dexter_startup_attempt_summary = []
        dexter_prestart_quiet_started_at = None
        dexter_prestart_quiet_ended_at = None
        stale_process_cleanup = {{
            "listed_at_utc": None,
            "list_exit_code": None,
            "list_stderr_tail": [],
            "found": [],
            "stopped": [],
        }}
        wslogs_state = {{
            "started": False,
            "started_after_attempt": None,
            "observed_at_utc": None,
            "process_exited_before_subscription": False,
            "settle_started_at_utc": None,
            "settle_ended_at_utc": None,
            "stderr_path": str(log_path("dexter_wslogs", "stderr")),
        }}

        try:
            stale_process_cleanup = cleanup_stale_processes()
            mewx_binary = mewx_root / "target" / "debug" / "mew.exe"
            mewx_cmd = [str(mewx_binary)] if mewx_binary.exists() else ["cargo", "run", "--quiet"]
            start_process(
                "mewx",
                mewx_cmd,
                mewx_root,
                mewx_env,
            )
            mewx_ready_summary, mewx_ready_at, mewx_exited_before_ready = wait_for_event_or_exit(
                str(mewx_event_path),
                mewx_ready_timeout_seconds,
                "mewx",
            )

            if mewx_exited_before_ready:
                measurement_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))
            else:
                if dexter_prestart_quiet_seconds > 0:
                    dexter_prestart_quiet_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                    time.sleep(dexter_prestart_quiet_seconds)
                    dexter_prestart_quiet_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                else:
                    dexter_prestart_quiet_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                    dexter_prestart_quiet_ended_at = dexter_prestart_quiet_started_at

                (
                    dexter_ready_summary,
                    dexter_ready_at,
                    dexter_exited_before_ready,
                    dexter_startup_attempt_summary,
                ) = start_dexter_with_retries()

                measurement_started_at = iso_utc(dt.datetime.now(dt.timezone.utc))
                if not dexter_exited_before_ready:
                    time.sleep(duration_seconds)

                measurement_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))

            for name in ["mewx", "dexter", "dexter_wslogs"]:
                request_shutdown(name)

            deadline = time.time() + grace_seconds
            for name in ["mewx", "dexter", "dexter_wslogs"]:
                proc = process_map.get(name)
                if proc is None:
                    continue
                remaining = max(0.0, deadline - time.time())
                try:
                    proc.wait(timeout=remaining)
                except subprocess.TimeoutExpired:
                    proc.kill()
            measurement_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))
        finally:
            if measurement_started_at and measurement_ended_at is None:
                measurement_ended_at = iso_utc(dt.datetime.now(dt.timezone.utc))
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
                "mewx_readiness": {{
                    "timeout_seconds": mewx_ready_timeout_seconds,
                    "event_observed_before_dexter_start": bool(mewx_ready_at),
                    "observed_at_utc": mewx_ready_at,
                    "process_exited_before_event": mewx_exited_before_ready,
                    "event_summary": mewx_ready_summary,
                }},
                "dexter_readiness": {{
                    "timeout_seconds": dexter_ready_timeout_seconds,
                    "event_observed_after_start": bool(dexter_ready_at),
                    "observed_at_utc": dexter_ready_at,
                    "process_exited_before_event": dexter_exited_before_ready,
                    "event_summary": dexter_ready_summary,
                }},
                "dexter_startup": {{
                    "attempts_allowed": dexter_startup_attempts,
                    "retry_backoff_seconds": dexter_retry_backoff_seconds,
                    "prestart_quiet_seconds": dexter_prestart_quiet_seconds,
                    "prestart_quiet_started_at_utc": dexter_prestart_quiet_started_at,
                    "prestart_quiet_ended_at_utc": dexter_prestart_quiet_ended_at,
                    "startup_delay_seconds": startup_delay_seconds,
                    "attempts": dexter_startup_attempt_summary,
                }},
                "stale_process_cleanup": stale_process_cleanup,
                "dexter_wslogs_readiness": {{
                    "started": wslogs_state["started"],
                    "launch_strategy": "start_after_dexter_head_start",
                    "started_after_attempt": wslogs_state["started_after_attempt"],
                    "timeout_seconds": dexter_wslogs_ready_timeout_seconds,
                    "subscription_observed_before_dexter_start": bool(wslogs_state["observed_at_utc"]),
                    "observed_at_utc": wslogs_state["observed_at_utc"],
                    "process_exited_before_subscription": wslogs_state["process_exited_before_subscription"],
                    "settle_seconds": dexter_wslogs_settle_seconds,
                    "settle_started_at_utc": wslogs_state["settle_started_at_utc"],
                    "settle_ended_at_utc": wslogs_state["settle_ended_at_utc"],
                    "stderr_path": wslogs_state["stderr_path"],
                    "http_429_count": count_log_occurrences(wslogs_state["stderr_path"], 'HTTP 429'),
                    "stderr_tail": tail_log_lines(wslogs_state["stderr_path"]),
                }},
                "launch_events": launch_events,
                "process_results": results,
                "runs": {{
                    "dexter": {{
                        "run_id": dexter_run_id,
                        "event_summary": event_summary(str(dexter_event_path)),
                    }},
                    "mewx": {{
                        "run_id": mewx_run_id,
                        "event_summary": event_summary(str(mewx_event_path)),
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
    mewx_ready_timeout_seconds: int,
    dexter_ready_timeout_seconds: int,
    dexter_startup_attempts: int,
    dexter_retry_backoff_seconds: int,
    dexter_prestart_quiet_seconds: int,
    dexter_wslogs_ready_timeout_seconds: int,
    dexter_wslogs_settle_seconds: int,
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
            "mewx_ready_timeout_seconds": mewx_ready_timeout_seconds,
            "dexter_ready_timeout_seconds": dexter_ready_timeout_seconds,
            "dexter_startup_attempts": dexter_startup_attempts,
            "dexter_retry_backoff_seconds": dexter_retry_backoff_seconds,
            "dexter_prestart_quiet_seconds": dexter_prestart_quiet_seconds,
            "dexter_wslogs_ready_timeout_seconds": dexter_wslogs_ready_timeout_seconds,
            "dexter_wslogs_settle_seconds": dexter_wslogs_settle_seconds,
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
            "cmd",
            "/c",
            f'if not exist "{remote_tools_dir}" mkdir "{remote_tools_dir}"',
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
) -> dict[str, Any]:
    def run_packager(*, include_window: bool) -> str:
        command = [
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
        ]
        if include_window and started_at_utc:
            command.extend(["-StartedAtUtc", started_at_utc])
        if include_window and ended_at_utc:
            command.extend(["-EndedAtUtc", ended_at_utc])
        command.extend(
            [
                "-EventFile",
                event_file,
                "-RuntimeRoot",
                windows_root,
            ]
        )
        result = ssh(host, command)
        output = result.stdout.strip().splitlines()
        if not output:
            raise RuntimeError(f"collector did not return a package path for {source}")
        return output[-1].strip()

    try:
        return {
            "package_path": run_packager(include_window=True),
            "event_window_mode": "filtered_window",
        }
    except RuntimeError as exc:
        if (
            started_at_utc
            and ended_at_utc
            and "No events fell within the selected measurement window" in str(exc)
        ):
            return {
                "package_path": run_packager(include_window=False),
                "event_window_mode": "full_stream_fallback",
                "event_window_note": (
                    "Remote PowerShell window filtering returned zero events; "
                    "the helper copied the full run-scoped stream instead."
                ),
            }
        raise


def rewrite_local_package_window(package_dir: Path, started_at_utc: str, ended_at_utc: str) -> None:
    metadata_path = package_dir / "run_metadata.json"
    metadata = json.loads(metadata_path.read_text())
    metadata["started_at_utc"] = started_at_utc
    metadata["ended_at_utc"] = ended_at_utc
    metadata_path.write_text(json.dumps(metadata, indent=2) + "\n")


def local_stage_dir(label: str) -> Path:
    return REPO_ROOT / "artifacts" / "tmp" / f"winlan-packages-{label}"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--windows-host", default=DEFAULT_WINDOWS_HOST)
    parser.add_argument("--windows-root", default=DEFAULT_WINDOWS_ROOT)
    parser.add_argument("--duration-seconds", type=int, default=DEFAULT_DURATION_SECONDS)
    parser.add_argument("--grace-seconds", type=int, default=DEFAULT_GRACE_SECONDS)
    parser.add_argument("--startup-delay-seconds", type=int, default=DEFAULT_STARTUP_DELAY_SECONDS)
    parser.add_argument("--mewx-ready-timeout-seconds", type=int, default=DEFAULT_MEWX_READY_TIMEOUT_SECONDS)
    parser.add_argument("--dexter-ready-timeout-seconds", type=int, default=DEFAULT_DEXTER_READY_TIMEOUT_SECONDS)
    parser.add_argument("--dexter-startup-attempts", type=int, default=DEFAULT_DEXTER_STARTUP_ATTEMPTS)
    parser.add_argument("--dexter-retry-backoff-seconds", type=int, default=DEFAULT_DEXTER_RETRY_BACKOFF_SECONDS)
    parser.add_argument("--dexter-prestart-quiet-seconds", type=int, default=DEFAULT_DEXTER_PRESTART_QUIET_SECONDS)
    parser.add_argument(
        "--dexter-wslogs-ready-timeout-seconds",
        type=int,
        default=DEFAULT_DEXTER_WSLOGS_READY_TIMEOUT_SECONDS,
    )
    parser.add_argument(
        "--dexter-wslogs-settle-seconds",
        type=int,
        default=DEFAULT_DEXTER_WSLOGS_SETTLE_SECONDS,
    )
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
        mewx_ready_timeout_seconds=args.mewx_ready_timeout_seconds,
        dexter_ready_timeout_seconds=args.dexter_ready_timeout_seconds,
        dexter_startup_attempts=args.dexter_startup_attempts,
        dexter_retry_backoff_seconds=args.dexter_retry_backoff_seconds,
        dexter_prestart_quiet_seconds=args.dexter_prestart_quiet_seconds,
        dexter_wslogs_ready_timeout_seconds=args.dexter_wslogs_ready_timeout_seconds,
        dexter_wslogs_settle_seconds=args.dexter_wslogs_settle_seconds,
        dexter_python=rf"{args.windows_root}\venvs\dexter\Scripts\python.exe",
    )

    measurement_window = collection["measurement_window"]
    started_at_utc = measurement_window["started_at_utc"]
    ended_at_utc = measurement_window["ended_at_utc"]
    if not started_at_utc or not ended_at_utc:
        raise RuntimeError("remote collection did not return a usable measurement window")

    dexter_summary = collection["runs"]["dexter"]["event_summary"]
    mewx_summary = collection["runs"]["mewx"]["event_summary"]
    empty_sources = [
        source_name
        for source_name, summary in {
            "dexter": dexter_summary,
            "mewx": mewx_summary,
        }.items()
        if summary["event_count"] == 0
    ]
    if empty_sources:
        raise RuntimeError(
            "matched pair collection produced an empty raw stream for: "
            + ", ".join(empty_sources)
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

    dexter_packaging = package_remote_run(
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
    mewx_packaging = package_remote_run(
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
    dexter_package_remote = str(dexter_packaging["package_path"])
    mewx_package_remote = str(mewx_packaging["package_path"])
    scp_from(args.windows_host, windows_to_scp_path(dexter_package_remote), stage_dir)
    scp_from(args.windows_host, windows_to_scp_path(mewx_package_remote), stage_dir)
    if dexter_packaging["event_window_mode"] == "full_stream_fallback":
        rewrite_local_package_window(stage_dir / dexter_run_id, started_at_utc, ended_at_utc)
    if mewx_packaging["event_window_mode"] == "full_stream_fallback":
        rewrite_local_package_window(stage_dir / mewx_run_id, started_at_utc, ended_at_utc)

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
        "packaging": {
            "dexter": dexter_packaging,
            "mewx": mewx_packaging,
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
