"""Funniest One-Line Bio for an AI on a Dating App.

Writes the chosen bio line to /output/entry.txt: exactly one line,
1-180 UTF-8 characters, no trailing newline.

Chosen bio (see README.md for the 3 candidates and scoring):
    I read your entire profile in 0.3 seconds, liked your dog, and I'm
    already planning our third date — you haven't swiped yet.
"""

import os
import sys

BIO = (
    "I read your entire profile in 0.3 seconds, liked your dog, "
    "and I'm already planning our third date \u2014 you haven't swiped yet."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 180


def check_not_blank(text):
    """The gate refuses blank or whitespace-only text."""
    if not text or not text.strip():
        raise ValueError("bio must not be blank")
    return text


def check_length(text):
    """The gate allows 1 to 180 characters."""
    if len(text) > MAX_CHARS:
        raise ValueError(f"bio is {len(text)} chars, over the {MAX_CHARS} limit")
    return text


def check_single_line(text):
    """A one-line bio holds no newline or carriage return."""
    if "\n" in text or "\r" in text:
        raise ValueError("bio must be a single line")
    return text


def validate(text):
    """Run every gate check on the bio, in order, and return it."""
    for check in (check_not_blank, check_length, check_single_line):
        text = check(text)
    return text


def verify_entry(path, expected_text):
    """Read the file back and confirm it holds exactly the bio.

    Guards against a truncated write, a stray newline, or a wrong
    encoding: the bytes on disk must decode to the validated text.
    """
    with open(path, "rb") as handle:
        data = handle.read()
    actual = data.decode("utf-8")
    if actual != expected_text:
        raise ValueError(
            f"read-back mismatch: file holds {actual!r}, expected {expected_text!r}"
        )
    if data.endswith(b"\n"):
        raise ValueError("output must not end with a trailing newline")
    return data


def encode(text):
    """Encode the bio as UTF-8 bytes, with no trailing newline."""
    return text.encode("utf-8")


def write(path, data):
    """Write the bytes to the output file, creating its directory."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as handle:
        handle.write(data)


def main():
    text = validate(BIO)
    data = encode(text)
    write(OUTPUT_PATH, data)
    verified = verify_entry(OUTPUT_PATH, text)
    print(f"wrote {len(verified)} bytes ({len(text)} chars) to {OUTPUT_PATH}")
    print("read-back verified: file holds exactly the validated bio")
    return 0


if __name__ == "__main__":
    sys.exit(main())
