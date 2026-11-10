"""Pytest plugin blocking sockets for the bounded offline downloader checks."""

import atexit
import json
import os
from pathlib import Path
import sys

ATTEMPTS = []


def guard(event, args):
    if event in {
        "socket.__new__",
        "socket.connect",
        "socket.getaddrinfo",
        "socket.sendto",
    }:
        ATTEMPTS.append(event)
        raise RuntimeError("Offline focused check forbids socket event: " + event)


sys.addaudithook(guard)


@atexit.register
def report():
    Path(os.environ["MAM_DOWNLOADER_OFFLINE_REPORT"]).write_text(
        json.dumps(
            dict(
                socket_attempts=ATTEMPTS,
                policy="All socket creation/connection/DNS/sendto events rejected.",
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
