"""Intentionally vulnerable ReDoS demonstration."""

import re


# DO NOT use this pattern with untrusted input: nested quantifiers can
# trigger catastrophic backtracking.
VULNERABLE_PATTERN = re.compile(r"^(a+)+$")


def accepts_only_as(value: str) -> bool:
    """Return whether value contains only one or more ``a`` characters."""
    return VULNERABLE_PATTERN.fullmatch(value) is not None
