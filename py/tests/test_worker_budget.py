"""Resource-policy fault injection; no corpus strings are transformed here."""

import ctypes
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from mb_cmn import worker_budget as wb


@pytest.mark.parametrize(
    "tasks,cpu,idle,memory,expected",
    [
        (39, 32, 32, 16384, 4),
        (2, 32, 32, 16384, 2),
        (39, 2, 2, 16384, 2),
        (39, 32, 1.9, 16384, 1),
        (39, 32, 0, 16384, 1),
        (39, 32, 32, 2048, 3),
        (39, 32, 32, 0, 1),
        (39, None, None, None, 2),
        (39, 32, None, 16384, 2),
        (39, 32, 32, None, 2),
    ],
)
def test_policy(monkeypatch, tasks, cpu, idle, memory, expected):
    monkeypatch.delenv("MAM_MAX_WORKERS", raising=False)
    monkeypatch.delenv("MAM_WORKER_MIB", raising=False)
    memory = memory * wb._MIB if memory is not None else None
    with (
        patch.object(wb, "resource_limits", return_value=(cpu, memory)),
        patch.object(wb, "idle_cpu_capacity", return_value=idle),
    ):
        assert wb.choose_workers(tasks) == expected


def test_configuration(monkeypatch):
    with (
        patch.object(wb, "resource_limits", return_value=(16, 4096 * wb._MIB)),
        patch.object(wb, "idle_cpu_capacity", return_value=16),
    ):
        monkeypatch.setenv("MAM_MAX_WORKERS", "8")
        monkeypatch.setenv("MAM_WORKER_MIB", "512")
        assert wb.choose_workers(39) == 6
        monkeypatch.setenv("MAM_WORKER_MIB", "1024")
        assert wb.choose_workers(39) == 3
        monkeypatch.setenv("MAM_MAX_WORKERS", "1")
        assert wb.choose_workers(39) == 1
        for bad in ("", "0", "-1", "1.5", "auto"):
            monkeypatch.setenv("MAM_MAX_WORKERS", bad)
            with pytest.raises(ValueError):
                wb.choose_workers(39)
        monkeypatch.setenv("MAM_MAX_WORKERS", "4")
        monkeypatch.setenv("MAM_WORKER_MIB", "bad")
        with pytest.raises(ValueError):
            wb.choose_workers(39)
    with pytest.raises(ValueError):
        wb.choose_workers(0)


def test_cgroup_limits(monkeypatch):
    files = {
        "/proc/self/cgroup": "0::/tenant/job\n",
        "/proc/self/mountinfo": "1 2 0:1 /tenant /cg rw - cgroup2 cgroup rw\n",
        "/proc/meminfo": "MemAvailable: 8388608 kB\n",
        "/cg/job/cpu.max": "max 100000",
        "/cg/cpu.max": "250000 100000",
        "/cg/job/memory.max": "max",
        "/cg/job/memory.current": "100",
        "/cg/memory.max": "1073741824",
        "/cg/memory.current": "268435456",
    }
    monkeypatch.setattr(
        wb, "_read_text", lambda path: files.get(Path(path).as_posix(), "")
    )
    assert wb._cgroup_directories() == [Path("/cg/job"), Path("/cg")]
    assert wb._linux_limits() == (2, 768 * wb._MIB)
    files["/cg/memory.current"] = "2147483648"
    assert wb._linux_limits() == (2, 0)
    files["/cg/cpu.max"] = "bad 0"
    files["/cg/memory.current"] = "bad"
    files["/proc/meminfo"] = "MemAvailable: 0 kB\n"
    assert wb._linux_limits() == (None, 0)
    files["/proc/self/cgroup"] = "0::/../../tenant/job\n"
    assert wb._cgroup_directories() == [Path("/cg")]
    files.clear()
    assert wb._linux_limits() == (None, None)


def test_linux_cpu_counters(monkeypatch):
    monkeypatch.setattr(wb.sys, "platform", "linux")
    monkeypatch.setattr(wb.os, "sched_getaffinity", lambda _: {1}, raising=False)
    monkeypatch.setattr(
        wb,
        "_read_text",
        lambda _: "cpu0 100 0 0 0 0 0 0 0\ncpu1 10 0 5 70 5 2 3 5 10 0\n",
    )
    assert wb._cpu_times() == (75, 100)
    monkeypatch.setattr(wb, "_linux_limits", lambda: (2, 123))
    assert wb.resource_limits() == (1, 123)


def test_dynamic_sample():
    with (
        patch.object(wb, "_cpu_times", side_effect=[(10, 100), (90, 200)]),
        patch.object(
            wb,
            "_quota_usage",
            side_effect=[{"/cg": (4, 100000)}, {"/cg": (4, 600000)}],
        ),
        patch.object(wb.time, "monotonic", side_effect=[1.0, 1.2]),
        patch.object(wb.time, "sleep") as sleep,
    ):
        assert wb.idle_cpu_capacity(4) == pytest.approx(1.5)
        sleep.assert_called_once_with(0.2)
    with patch.object(wb, "_cpu_times", return_value=None):
        assert wb.idle_cpu_capacity(4) is None


def test_missing_detection(monkeypatch):
    monkeypatch.setattr(wb.sys, "platform", "unknown")
    monkeypatch.setattr(wb.os, "process_cpu_count", lambda: None, raising=False)

    def unavailable(_):
        raise OSError("unavailable")

    monkeypatch.setattr(wb.os, "sched_getaffinity", unavailable, raising=False)
    assert wb.resource_limits() == (None, None)
    assert wb._cpu_times() is None


def test_invalid_counter_delta():
    for after in ((5, 200), (200, 200), (20, 100)):
        with (
            patch.object(wb, "_cpu_times", side_effect=[(10, 100), after]),
            patch.object(wb, "_quota_usage", return_value={}),
            patch.object(wb.time, "monotonic", side_effect=[1.0, 1.2]),
            patch.object(wb.time, "sleep"),
        ):
            assert wb.idle_cpu_capacity(4) is None


def test_windows_apis(monkeypatch):
    def memory(pointer):
        assert pointer._obj.length == 64
        pointer._obj.available = 123456789
        return 1

    def times(idle, kernel, user):
        idle._obj.value, kernel._obj.value, user._obj.value = 20, 30, 10
        return 1

    kernel = SimpleNamespace(GlobalMemoryStatusEx=memory, GetSystemTimes=times)
    monkeypatch.setattr(
        ctypes, "windll", SimpleNamespace(kernel32=kernel), raising=False
    )
    monkeypatch.setattr(wb.sys, "platform", "win32")
    assert wb._windows_available_memory() == 123456789
    assert wb._cpu_times() == (20, 40)
    kernel.GlobalMemoryStatusEx = lambda _: 0
    kernel.GetSystemTimes = lambda *_: 0
    assert wb._windows_available_memory() is None
    assert wb._cpu_times() is None
    monkeypatch.delattr(ctypes, "windll")
    assert wb._windows_available_memory() is None
    assert wb._cpu_times() is None


def test_serial_foi_bypasses_budget(monkeypatch):
    import main_foi_features_of_interest as foi

    monkeypatch.setenv("MAM_MAX_WORKERS", "invalid")
    monkeypatch.setattr(foi.tbn, "ALL_BK39_IDS", ["book"])
    monkeypatch.setattr(foi, "find_wt_fois_for_1_bk", lambda _: ("book", []))
    monkeypatch.setattr(foi.fct, "record_fois_for_1_bk", lambda *_: None)
    foi._do_wikitext_features_of_interest(None, True, {"book": []}, {})
