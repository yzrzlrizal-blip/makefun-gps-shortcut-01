"""The GPS Swears It Was a Shortcut — make.fun entry.

Writes the GPS's one-line excuse to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).
"""

import os
import tempfile

ENTRY = (
    "The map promised a shortcut, so I took you through a cul-de-sac "
    "straight into a wedding \u2014 relax, the bride waved, and honestly "
    "we were the best entrance they had."
)


def check_entry(text: str) -> None:
    """Validate the entry line before writing it out.

    Mirrors the competition gate: UTF-8 text of 1-200 characters, not
    only whitespace, a single line, and no control characters at all
    (including DEL and tab, which would break the one-line plain-text
    reading of the entry).
    """
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if text.strip() == "":
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8 text


def main() -> None:
    check_entry(ENTRY)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    # MAKEFUN_OUTPUT_DIR is a directory; default target is /output/entry.txt.
    if out_dir.endswith("entry.txt"):
        target = out_dir
        directory = os.path.dirname(target) or "."
    else:
        directory = out_dir
        target = os.path.join(directory, "entry.txt")
    os.makedirs(directory, exist_ok=True)
    data = ENTRY.encode("utf-8")
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
        os.replace(tmp_path, target)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
    # Re-read and verify the written bytes.
    with open(target, "rb") as fh:
        written = fh.read()
    if written != data:
        raise ValueError("verification failed: written bytes differ from entry")


if __name__ == "__main__":
    main()
