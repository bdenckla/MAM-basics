"""Bounded offline completion-spacing/concurrency probes of exact downloader bytes."""

import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import threading
import time
from urllib.parse import urlsplit

import requests

SOURCE, BASE_SOURCE, OUT = map(Path, sys.argv[1:4])
ATTEMPTS = []


def guard(event, args):
    if event in {
        "socket.__new__",
        "socket.connect",
        "socket.getaddrinfo",
        "socket.sendto",
    }:
        ATTEMPTS.append(event)
        raise RuntimeError("Offline probe forbids socket event: " + event)


sys.addaudithook(guard)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


head = load(SOURCE, "focused_downloader_head")
base = load(BASE_SOURCE, "focused_downloader_base")


class Clock:
    def __init__(self, first_sleep_scale=1):
        self.now = 0.0
        self.sleeps = []
        self.lock = threading.Lock()
        self.first_sleep_scale = first_sleep_scale

    def monotonic(self):
        with self.lock:
            return self.now

    def advance(self, seconds):
        with self.lock:
            self.now += seconds

    def sleep(self, seconds):
        with self.lock:
            factor = self.first_sleep_scale if not self.sleeps else 1
            self.sleeps.append(seconds)
            self.now += seconds * factor


class Reply:
    def __init__(self, url, body=b"ok", target=None):
        self.url, self.content = url, body
        self.status_code = 302 if target else 200
        self.headers = {"Location": target} if target else {}
        self.encoding = self.apparent_encoding = "utf-8"
        self.next = requests.Request("GET", target).prepare() if target else None

    def raise_for_status(self):
        assert self.status_code < 400


class Session:
    def __init__(self, clock, behavior=None, duration=5):
        self.clock, self.behavior, self.duration = clock, behavior, duration
        self.headers, self.records = {}, []
        self.max_redirects = 10

    def request(self, method, url, **kwargs):
        assert kwargs.get("allow_redirects") in (None, False)
        start = self.clock.monotonic()
        record = dict(url=url, host=urlsplit(url).hostname, start=start)
        self.records.append(record)
        try:
            if self.behavior:
                return self.behavior(url, len(self.records))
            self.clock.advance(self.duration)
            return Reply(url)
        finally:
            record["end"] = self.clock.monotonic()

    def send(self, request, **kwargs):
        return self.request(request.method, request.url, **kwargs)

    def merge_environment_settings(self, *args):
        return {}

    def close(self):
        pass


def downloader(module, clock, session, delay=2, attempts=1, robots=False):
    config = module.PoliteDownloadConfig(
        user_agent="OfflineProbe/1.0",
        throttle=module.ThrottleConfig(min_delay_s=delay),
        retry=module.RetryConfig(max_attempts=attempts, first_backoff_s=1),
        obey_robots_txt=robots,
    )
    return module.PoliteDownloader(
        config, session=session, monotonic_fun=clock.monotonic, sleep_fun=clock.sleep
    )


def spacing(records, delay=2):
    previous = {}
    for record in records:
        host = record["host"]
        if host in previous:
            assert record["start"] >= previous[host] + delay, records
        previous[host] = record["end"]


started = time.perf_counter()
checks = []
try:
    # Differential oracle: a long response exposes the old start-based spacing.
    differences = {}
    for label, module in [("base", base), ("head", head)]:
        clock = Clock()
        session = Session(clock)
        client = downloader(module, clock, session)
        client.get_text("https://sequential.test/a")
        client.get_text("https://sequential.test/b")
        gap = session.records[1]["start"] - session.records[0]["end"]
        differences[label] = dict(
            completion_gap=gap, records=session.records, sleeps=clock.sleeps
        )
    assert differences["base"]["completion_gap"] == 0
    assert differences["head"]["completion_gap"] == 2
    checks.append(
        dict(
            case="long-response completion spacing, differential against exact base",
            result="PASS",
            observations=differences,
        )
    )

    for factor in (0.125, 2):
        clock = Clock(first_sleep_scale=factor)
        session = Session(clock)
        client = downloader(head, clock, session)
        client.get_text("https://sleep.test/a")
        client.get_text("https://sleep.test/b")
        spacing(session.records)
        assert len(clock.sleeps) == (2 if factor < 1 else 1)
        checks.append(
            dict(
                case=f"early/late sleep, first scale {factor}",
                result="PASS",
                records=session.records,
                sleeps=clock.sleeps,
            )
        )

    clock = Clock()
    session = Session(clock, duration=7)
    first = downloader(head, clock, session, delay=0)
    second = downloader(head, clock, session, delay=3)
    first.get_text("http://EXAMPLE.test/a")
    second.get_text("https://example.test:8443/b")
    spacing(session.records, 3)
    assert session.records[1]["start"] == 10
    checks.append(
        dict(
            case="shared clock across downloader instances, zero-delay predecessor and normalized host/ports",
            result="PASS",
            records=session.records,
        )
    )

    clock_a, clock_b = Clock(), Clock()
    session_a, session_b = Session(clock_a), Session(clock_b)
    downloader(head, clock_a, session_a).get_text("https://clocks.test/a")
    downloader(head, clock_b, session_b).get_text("https://clocks.test/b")
    assert session_b.records[0]["start"] == 0 and not clock_b.sleeps
    checks.append(dict(case="separate injected clocks remain isolated", result="PASS"))

    clock = Clock()

    def timeout_then_success(url, call):
        clock.advance(5)
        if call == 1:
            raise requests.Timeout("synthetic offline timeout")
        return Reply(url)

    session = Session(clock, timeout_then_success)
    assert (
        downloader(head, clock, session, attempts=2).get_text("https://retry.test/a")
        == "ok"
    )
    spacing(session.records)
    assert clock.sleeps == [1, 1]
    checks.append(
        dict(
            case="failed response completion still spaces retry, independently of backoff",
            result="PASS",
            records=session.records,
            sleeps=clock.sleeps,
        )
    )

    clock = Clock()

    def routing(url, call):
        path = urlsplit(url).path
        clock.advance(3 if path == "/robots.txt" else 7)
        if path == "/robots.txt":
            return Reply(url, body=b"User-agent: *\nAllow: /\n")
        target = {
            "https://a.test/start": "https://b.test/hop",
            "https://b.test/hop": "https://a.test/final",
        }.get(url)
        return Reply(url, target=target)

    session = Session(clock, routing)
    assert (
        downloader(head, clock, session, robots=True).get_text("https://a.test/start")
        == "ok"
    )
    assert len(session.records) == 5
    spacing(session.records)
    checks.append(
        dict(
            case="robots reads and cross-host redirect hops all respect completion spacing",
            result="PASS",
            records=session.records,
        )
    )

    for different_host in (False, True):
        clock = Clock()
        entered_first, release_first, entered_second, attempted_second = (
            threading.Event() for _ in range(4)
        )
        errors = []

        def first_behavior(url, call):
            entered_first.set()
            assert release_first.wait(2), "probe did not release held response"
            clock.advance(5)
            return Reply(url)

        def second_behavior(url, call):
            entered_second.set()
            clock.advance(1)
            return Reply(url)

        one, two = Session(clock, first_behavior), Session(clock, second_behavior)
        client_one, client_two = downloader(head, clock, one), downloader(
            head, clock, two
        )

        def worker(client, url, attempt=None):
            try:
                if attempt:
                    attempt.set()
                client.get_text(url)
            except BaseException as error:
                errors.append(repr(error))

        t1 = threading.Thread(
            target=worker, args=(client_one, "https://held.test/a"), daemon=True
        )
        url_two = (
            "https://other.test/b" if different_host else "http://HELD.test:8080/b"
        )
        t2 = threading.Thread(
            target=worker, args=(client_two, url_two, attempted_second), daemon=True
        )
        t1.start()
        assert entered_first.wait(1)
        t2.start()
        assert attempted_second.wait(1)
        try:
            entered_while_held = entered_second.wait(0.5 if different_host else 0.05)
            assert entered_while_held == different_host
        finally:
            release_first.set()
            t1.join(2)
            t2.join(2)
        assert not t1.is_alive() and not t2.is_alive() and not errors, errors
        if not different_host:
            spacing(one.records + two.records)
            assert two.records[0]["start"] == one.records[0]["end"] + 2
        checks.append(
            dict(
                case=(
                    "different hosts progress independently"
                    if different_host
                    else "same host serializes concurrent downloader instances through response completion"
                ),
                result="PASS",
                second_entered_while_first_held=entered_while_held,
                records=one.records + two.records,
            )
        )
    result = dict(
        result="PASS",
        source=str(SOURCE),
        source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        base_source_sha256=hashlib.sha256(BASE_SOURCE.read_bytes()).hexdigest(),
        cases=len(checks),
        checks=checks,
        elapsed_seconds=round(time.perf_counter() - started, 6),
        socket_attempts=ATTEMPTS,
        limits="Offline fake sessions and controlled clocks/events only; no live-host, interprocess, or arbitrary external session request guarantee.",
    )
except BaseException as error:
    import traceback

    result = dict(
        result="FAIL",
        error=repr(error),
        traceback=traceback.format_exc(),
        completed_checks=checks,
        socket_attempts=ATTEMPTS,
    )
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    raise
OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(
    json.dumps(
        dict(
            result=result["result"],
            cases=result["cases"],
            elapsed_seconds=result["elapsed_seconds"],
            socket_attempts=ATTEMPTS,
        ),
        indent=2,
    )
)
