#!/usr/bin/env python3
"""make.fun bounty entry: u-coral-404-one-liner-laughs-aa872d41.

Writes a single original one-line joke (max 200 characters) to the
entry output file and verifies it by reading it back.
"""

import os
import sys

ENTRY = "I asked my Wi-Fi router for some space — it took it personally, and now we're on a break every five minutes."

OUTPUT_PATH = os.path.expanduser(
    "~/workspace/make-fun/entries/u-coral-404-one-liner-laughs-aa872d41/entry-output.txt"
)

MAX_CHARS = 200


def validate(text: str) -> None:
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, exceeds {MAX_CHARS}")
    if not text.strip():
        raise ValueError("entry must not be empty")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    print(f"entry length: {len(text)} characters (max {MAX_CHARS})", file=sys.stderr)


def write_entry(path: str, text: str) -> None:
    """Write the entry, falling back to a sibling path if the primary fails."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text + "\n")
    except OSError:
        fallback = path + ".fallback"
        print(f"primary write failed, using fallback {fallback}", file=sys.stderr)
        with open(fallback, "w", encoding="utf-8") as f:
            f.write(text + "\n")


def main() -> int:
    validate(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    write_entry(OUTPUT_PATH, ENTRY)
    # Read-back verification: the file must contain exactly the entry.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        read_back = f.read()
    if read_back != ENTRY + "\n":
        raise ValueError("read-back verification failed: file content mismatch")
    # Second verification: the read-back text itself must still pass validation.
    validate(read_back.rstrip("\n"))
    print("read-back verification passed", file=sys.stderr)
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
