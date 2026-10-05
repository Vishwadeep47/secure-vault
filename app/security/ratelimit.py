"""Brute-force lockout (in memory).

Limitation: state resets when the server restarts. Use Redis or a database table
if you need it to persist.
"""
import threading
import time

from flask import current_app

_lock = threading.Lock()
_failures = {}  # username -> (failure_count, first_failure_timestamp)


def is_locked(username):
    cfg = current_app.config
    with _lock:
        count, first = _failures.get(username, (0, 0.0))
        if count >= cfg["MAX_FAILED_LOGINS"]:
            if time.time() - first < cfg["LOCKOUT_SECONDS"]:
                return True
            _failures.pop(username, None)
    return False


def register_failure(username):
    with _lock:
        count, first = _failures.get(username, (0, time.time()))
        _failures[username] = (count + 1, first)


def clear_failures(username):
    with _lock:
        _failures.pop(username, None)


_hits = {}  # key -> list of request timestamps


def too_many_requests(key, limit, window_seconds):
    """Count a request for `key`; return True if it exceeds `limit` per window."""
    now = time.time()
    with _lock:
        recent = [t for t in _hits.get(key, []) if now - t < window_seconds]
        if len(recent) >= limit:
            _hits[key] = recent
            return True
        recent.append(now)
        _hits[key] = recent
        return False


def clear_all():
    """Forget everything (used by tests)."""
    with _lock:
        _failures.clear()
        _hits.clear()
