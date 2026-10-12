"""A validated, interruptible command-line countdown timer."""
from __future__ import annotations

import argparse
import re
import time
from collections.abc import Callable

DURATION_RE = re.compile(r"^(?:(?P<hours>\d+):)?(?P<minutes>\d{1,2}):(?P<seconds>\d{1,2})$")


def parse_duration(value: str) -> int:
    """Parse SS, MM:SS, or HH:MM:SS into seconds; require clock fields < 60."""
    text = value.strip()
    if text.isdigit():
        seconds = int(text)
    else:
        match = DURATION_RE.fullmatch(text)
        if match is None:
            raise ValueError("Use seconds, MM:SS, or HH:MM:SS.")
        minutes, seconds = int(match.group("minutes")), int(match.group("seconds"))
        hours = int(match.group("hours") or 0)
        if seconds >= 60 or minutes >= 60:
            raise ValueError("Minutes and seconds in clock format must be below 60.")
        seconds += minutes * 60 + hours * 3600
    if seconds <= 0:
        raise ValueError("Duration must be greater than zero.")
    if seconds > 99 * 3600 + 59 * 60 + 59:
        raise ValueError("Maximum duration is 99:59:59.")
    return seconds


def format_duration(seconds: int) -> str:
    """Format non-negative whole seconds as HH:MM:SS."""
    if not isinstance(seconds, int) or seconds < 0:
        raise ValueError("Duration must be a non-negative whole number of seconds.")
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def countdown(
    duration_seconds: int,
    *,
    sleep_fn: Callable[[float], None] = time.sleep,
    clock_fn: Callable[[], float] = time.monotonic,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Display remaining time at one-second intervals, then notify on expiry."""
    if not isinstance(duration_seconds, int) or duration_seconds <= 0:
        raise ValueError("Duration must be a positive whole number of seconds.")
    deadline = clock_fn() + duration_seconds
    remaining = duration_seconds
    while remaining > 0:
        output_fn(format_duration(remaining))
        sleep_fn(min(1.0, max(0.0, deadline - clock_fn())))
        remaining = max(0, int(deadline - clock_fn() + 0.999999))
    output_fn("Time is up!")
    try:
        print("\a", end="", flush=True)
    except (OSError, RuntimeError):
        pass


def main() -> None:
    parser = argparse.ArgumentParser(description="Count down a duration and notify at expiry.")
    parser.add_argument("duration", nargs="?", help="seconds, MM:SS, or HH:MM:SS")
    args = parser.parse_args()
    raw = args.duration
    if raw is None:
        raw = input("Duration (seconds, MM:SS, or HH:MM:SS): ")
    try:
        duration = parse_duration(raw)
    except ValueError as error:
        parser.error(str(error))
    print(f"Starting {format_duration(duration)} countdown. Press Ctrl+C to stop.")
    try:
        countdown(duration)
    except KeyboardInterrupt:
        print("\nCountdown cancelled.")


if __name__ == "__main__":
    main()