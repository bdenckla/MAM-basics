"""Conservative, per-pool limits; see doc/internal-worker-budget.md.

This is not a reservation or a scheduler shared between independent runs.
Private consumers vendor this file verbatim; no cross-tree runtime imports.
"""

import ctypes
import os
from pathlib import Path
import sys
import time

_MIB = 1024 * 1024


def _read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except OSError:
        return ""


def _positive_int(value):
    try:
        number = int(value)
    except (ValueError, TypeError):
        return None
    return number if number > 0 else None


def _configured(name, default):
    value = os.environ.get(name)
    if value is None:
        return default
    number = _positive_int(value)
    if number is None:
        raise ValueError(f"{name} must be a positive integer, got {value!r}")
    return number


def _cgroup_directories():
    """Current cgroup-v2 directory and visible ancestors, from kernel metadata."""
    group = next(
        (
            line[3:]
            for line in _read_text("/proc/self/cgroup").splitlines()
            if line.startswith("0::")
        ),
        None,
    )
    if group is None:
        return []
    directories = []
    for line in _read_text("/proc/self/mountinfo").splitlines():
        left, separator, right = line.partition(" - ")
        fields = left.split()
        if (
            not separator
            or not right.split()
            or right.split()[0] != "cgroup2"
            or len(fields) < 5
        ):
            continue
        # Kernel mountinfo escapes unusual path characters with octal sequences.
        # Ignore such mounts rather than guessing their path.
        if "\\" in fields[3] or "\\" in fields[4]:
            continue
        root, mount = Path(fields[3]), Path(fields[4])
        current = (
            mount / Path(group).relative_to(root)
            if ".." not in Path(group).parts and Path(group).is_relative_to(root)
            else mount
        )
        while current.is_relative_to(mount):
            directories.append(current)
            if current == mount:
                break
            current = current.parent
    return directories


def _linux_limits():
    """Return CPU quota and currently available bytes; unknown limits are None."""
    cpus, memory = [], []
    for line in _read_text("/proc/meminfo").splitlines():
        fields = line.split()
        if len(fields) == 3 and fields[0] == "MemAvailable:" and fields[2] == "kB":
            try:
                value = int(fields[1])
            except ValueError:
                continue
            if value >= 0:
                memory.append(value * 1024)
    for directory in _cgroup_directories():
        quota = _read_text(directory / "cpu.max").split()
        if len(quota) == 2:
            numerator, denominator = map(_positive_int, quota)
            if numerator is not None and denominator is not None:
                cpus.append(max(1, numerator // denominator))
        limit = _positive_int(_read_text(directory / "memory.max").strip())
        try:
            used = int(_read_text(directory / "memory.current").strip())
        except ValueError:
            used = -1
        if limit is not None and used >= 0:
            memory.append(max(0, limit - used))
    return min(cpus, default=None), min(memory, default=None)


def _windows_available_memory():
    """Available physical memory, using the Windows API without a dependency."""

    class MemoryStatus(ctypes.Structure):
        _fields_ = [("length", ctypes.c_uint32), ("load", ctypes.c_uint32)] + [
            (name, ctypes.c_uint64)
            for name in (
                "total",
                "available",
                "page_total",
                "page_available",
                "virtual_total",
                "virtual_available",
                "extended",
            )
        ]

    status = MemoryStatus()
    status.length = ctypes.sizeof(status)
    try:
        succeeded = ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status))
    except (AttributeError, OSError):
        return None
    return status.available if succeeded else None


def resource_limits():
    """Detect usable logical CPUs and available memory, without assuming idle CPUs."""
    cpu = _positive_int(getattr(os, "process_cpu_count", os.cpu_count)())
    if hasattr(os, "sched_getaffinity"):
        try:
            affinity = len(os.sched_getaffinity(0))
            cpu = min(cpu, affinity) if cpu and affinity else cpu or affinity or None
        except OSError:
            pass
    memory = None
    if sys.platform == "linux":
        quota, memory = _linux_limits()
        if quota is not None:
            cpu = min(cpu, quota) if cpu else quota
    elif sys.platform == "win32":
        memory = _windows_available_memory()
    return cpu, memory


def _cpu_times():
    """Return cumulative idle/total counters, using affinity on Linux."""
    if sys.platform == "win32":
        idle, kernel, user = ctypes.c_uint64(), ctypes.c_uint64(), ctypes.c_uint64()
        try:
            ok = ctypes.windll.kernel32.GetSystemTimes(
                ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)
            )
        except (AttributeError, OSError):
            return None
        return (idle.value, kernel.value + user.value) if ok else None
    if sys.platform != "linux":
        return None
    try:
        affinity = os.sched_getaffinity(0)
    except (AttributeError, OSError):
        affinity = None
    idle = total = 0
    for line in _read_text("/proc/stat").splitlines():
        fields = line.split()
        if not fields or not fields[0].startswith("cpu") or not fields[0][3:].isdigit():
            continue
        if affinity is not None and int(fields[0][3:]) not in affinity:
            continue
        try:
            ticks = list(map(int, fields[1:9]))
        except ValueError:
            return None
        if len(ticks) < 5:
            return None
        idle += ticks[3] + ticks[4]
        total += sum(ticks)
    return (idle, total) if total else None


def _quota_usage():
    """Cumulative CPU microseconds for each visible finite cgroup-v2 quota."""
    result = {}
    if sys.platform != "linux":
        return result
    for directory in _cgroup_directories():
        fields = _read_text(directory / "cpu.max").split()
        if len(fields) != 2:
            continue
        quota, period = map(_positive_int, fields)
        if quota is None or period is None:
            continue
        for line in _read_text(directory / "cpu.stat").splitlines():
            pair = line.split()
            if len(pair) == 2 and pair[0] == "usage_usec":
                try:
                    used = int(pair[1])
                except ValueError:
                    continue
                if used >= 0:
                    result[str(directory)] = (quota / period, used)
    return result


def idle_cpu_capacity(cpu_limit):
    """Sample current capacity for 200 ms; unknown counters return None."""
    before, groups_before = _cpu_times(), _quota_usage()
    if before is None:
        return None
    start = time.monotonic()
    time.sleep(0.2)
    after, groups_after = _cpu_times(), _quota_usage()
    elapsed = time.monotonic() - start
    if after is None or elapsed <= 0:
        return None
    idle, total = after[0] - before[0], after[1] - before[1]
    if total <= 0 or not 0 <= idle <= total:
        return None
    capacity = cpu_limit * idle / total
    for group, (quota, used) in groups_after.items():
        previous = groups_before.get(group)
        if previous is not None and previous[0] == quota and used >= previous[1]:
            capacity = min(
                capacity, max(0, quota - (used - previous[1]) / (elapsed * 1e6))
            )
    return capacity


def choose_workers(task_count, *, worker_mib=512):
    """Choose a bounded pool size; explicit serial paths need not call this function.

    MAM_MAX_WORKERS changes the default ceiling of four, not resource limits.
    MAM_WORKER_MIB overrides the per-worker memory estimate. Unknown CPU, load or memory
    information imposes a two-worker fallback ceiling. At least one worker is
    returned for nonempty work, even if the memory estimate cannot be satisfied.
    """
    if task_count < 1 or worker_mib < 1:
        raise ValueError("task_count and worker_mib must be positive")
    ceiling = _configured("MAM_MAX_WORKERS", 4)
    estimate = _configured("MAM_WORKER_MIB", worker_mib) * _MIB
    cpu, available = resource_limits()
    limits = [task_count, ceiling, cpu if cpu is not None else 2]
    idle = idle_cpu_capacity(cpu) if cpu is not None else None
    limits.append(max(1, int(idle)) if idle is not None else 2)
    if available is None:
        limits.append(2)
    else:
        reserve = max(512 * _MIB, available // 4)
        limits.append(max(1, (available - reserve) // estimate))
    return max(1, min(limits))
