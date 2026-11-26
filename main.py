#!/usr/bin/env python3
"""One-liner entry: Wi-Fi router joke.

Writes the entry text to the make.fun output location and prints it to
stdout. Output resolution (first success wins):
  1. $MAKEFUN_OUTPUT_DIR - a directory; entry.txt is written inside it.
  2. $MAKEFUN_OUTPUT     - a file path.
  3. /tmp/u-coral-404-one-liner-laughs-aa872d41/entry.txt (per-entry fallback).
Never writes into the repository directory or a home directory.
"""

import os
import sys

ENTRY = "I asked my Wi-Fi router for some space — it took it personally, and now we're on a break every five minutes."

# Competition limit for a one-liner entry.
MAX_LENGTH = 200

# Last-resort output location. The grader may run as an unprivileged user
# on a read-only filesystem with no home directory, so the fallback must
# not depend on $HOME or on the repository directory; /tmp is writable
# there and is namespaced per entry to avoid collisions.
FALLBACK_PATH = "/tmp/u-coral-404-one-liner-laughs-aa872d41/entry.txt"


def candidate_paths():
    """Return the ordered list of output paths to try."""
    paths = []
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    if out_dir:
        paths.append(os.path.join(out_dir, "entry.txt"))
    out_file = os.environ.get("MAKEFUN_OUTPUT", "").strip()
    if out_file:
        paths.append(out_file)
    paths.append(FALLBACK_PATH)
    return paths


def validate_entry(text):
    """Check the entry is a single line, <= 200 chars, ending in punctuation."""
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if len(text) > MAX_LENGTH:
        raise ValueError("entry exceeds %d characters" % MAX_LENGTH)
    if not text or text[-1] not in ".!?":
        raise ValueError("entry must end with sentence-ending punctuation")
    return text


def write_entry(text):
    """Write the entry to the first writable candidate path.

    Returns the path written. Each candidate's parent directory is created
    first; an OSError on one candidate falls through to the next.
    """
    last_error = None
    for path in candidate_paths():
        try:
            parent = os.path.dirname(path)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text + "\n")
            # Read-back verification: the file must contain exactly the entry.
            with open(path, "r", encoding="utf-8") as handle:
                written = handle.read()
            if written != text + "\n":
                raise OSError("read-back mismatch for %s" % path)
            return path
        except OSError as exc:
            last_error = exc
    raise last_error


def main():
    entry = validate_entry(ENTRY)
    write_entry(entry)
    sys.stdout.write(entry + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
