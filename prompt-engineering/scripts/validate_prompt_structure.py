"""Validate a canonical structured prompt without calling an LLM.

This utility checks heading names, required sections, canonical rendering order,
bullet-list requirements for instructions and constraints, framework-specific
timestamp usage, and optionally declared runtime variables. It validates prompt
structure only; it does not prove semantic correctness or model behavior.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CANONICAL_FIELDS = [
    "ROLE",
    "OBJECTIVE",
    "INSTRUCTION",
    "CAPABILITY",
    "CONTEXT",
    "INPUT",
    "OUTPUT_LANGUAGE",
    "OUTPUT_DATATYPE",
    "OUTPUT_FORMAT",
    "OUTPUT_EXAMPLE",
    "CONSTRAINT",
]
REQUIRED_FIELDS = {
    "ROLE",
    "OBJECTIVE",
    "INSTRUCTION",
    "CONTEXT",
    "INPUT",
    "OUTPUT_DATATYPE",
    "OUTPUT_FORMAT",
    "OUTPUT_EXAMPLE",
    "CONSTRAINT",
}
FIELD_PATTERN = re.compile(
    r"^(?:#{1,6}\s+|\[)(ROLE|OBJECTIVE|INSTRUCTION|CAPABILITY|CONTEXT|INPUT|"
    r"OUTPUT_LANGUAGE|OUTPUT_DATATYPE|OUTPUT_FORMAT|OUTPUT_EXAMPLE|CONSTRAINT|"
    r"_TIMESTAMP)(?:\])?\s*$"
)
PLACEHOLDER_PATTERN = re.compile(r"{{([A-Za-z_][A-Za-z0-9_]*)}}")


def parse_arguments() -> argparse.Namespace:
    """Parse command-line options for a prompt structure validation run.

    Returns:
        Parsed command-line arguments, including the prompt path, the selected
        framework mode, and optional runtime variables declared by the caller.
    """
    parser = argparse.ArgumentParser(
        description="Validate canonical prompt headings, ordering, and variables."
    )
    parser.add_argument("prompt_file", type=Path, help="Canonical Markdown prompt file.")
    parser.add_argument(
        "--prompt4py",
        action="store_true",
        help="Allow the framework-generated _TIMESTAMP heading.",
    )
    parser.add_argument(
        "--provided",
        action="append",
        default=[],
        metavar="VARIABLE",
        help="Runtime placeholder supplied by the caller; repeat as needed.",
    )
    return parser.parse_args()


def parse_sections(text: str) -> tuple[list[str], dict[str, list[str]]]:
    """Extract canonical heading sections and their non-heading body lines.

    Args:
        text: UTF-8 prompt document content.

    Returns:
        A tuple containing the field order found in the document and a mapping
        from field names to their body lines.
    """
    order: list[str] = []
    sections: dict[str, list[str]] = {}
    current_field: str | None = None

    for line in text.splitlines():
        match = FIELD_PATTERN.match(line.strip())
        if match:
            current_field = match.group(1)
            order.append(current_field)
            sections.setdefault(current_field, [])
            continue
        if current_field is not None:
            sections[current_field].append(line)

    return order, sections


def section_has_content(lines: list[str]) -> bool:
    """Determine whether a section contains meaningful content.

    Args:
        lines: Body lines collected below a canonical heading.

    Returns:
        True when at least one non-empty line appears in the section.
    """
    return any(line.strip() for line in lines)


def section_has_bullets(lines: list[str]) -> bool:
    """Determine whether a list-oriented section contains Markdown bullets.

    Args:
        lines: Body lines collected below a canonical heading.

    Returns:
        True when a bullet item is present.
    """
    return any(re.match(r"^\s*[-*+]\s+\S", line) for line in lines)


def validate_structure(
    order: list[str],
    sections: dict[str, list[str]],
    prompt4py: bool,
    provided_variables: set[str],
    text: str,
) -> list[str]:
    """Validate the prompt contract and return actionable error messages.

    Args:
        order: Field headings in the sequence found in the document.
        sections: Body lines grouped by field heading.
        prompt4py: Whether framework-generated timestamp support is enabled.
        provided_variables: Runtime variable names declared by the caller.
        text: Full prompt text used to discover placeholders.

    Returns:
        A list of validation errors. An empty list indicates structural success.
    """
    errors: list[str] = []
    duplicates = sorted({field for field in order if order.count(field) > 1})
    if duplicates:
        errors.append(f"Repeated canonical headings: {', '.join(duplicates)}.")

    if "_TIMESTAMP" in order and not prompt4py:
        errors.append("_TIMESTAMP is only allowed with --prompt4py.")

    present_fields = [field for field in order if field in CANONICAL_FIELDS]
    expected_order = [field for field in CANONICAL_FIELDS if field in present_fields]
    if present_fields != expected_order:
        errors.append(
            "Canonical fields are out of order. Expected relative order: "
            + " -> ".join(CANONICAL_FIELDS)
            + "."
        )

    missing_fields = sorted(REQUIRED_FIELDS.difference(sections))
    if missing_fields:
        errors.append(f"Missing required fields: {', '.join(missing_fields)}.")

    for field in REQUIRED_FIELDS.intersection(sections):
        if not section_has_content(sections[field]):
            errors.append(f"{field} must contain meaningful content.")

    for field in ("INSTRUCTION", "CONSTRAINT"):
        if field in sections and not section_has_bullets(sections[field]):
            errors.append(f"{field} must use a Markdown bullet list of atomic items.")

    placeholders = set(PLACEHOLDER_PATTERN.findall(text))
    if provided_variables:
        missing_variables = sorted(placeholders.difference(provided_variables))
        if missing_variables:
            errors.append(
                "Undeclared runtime placeholders: " + ", ".join(missing_variables) + "."
            )

    return errors


def main() -> int:
    """Run the command-line validator and print the validation result.

    Returns:
        Process exit code zero for structural success and one for validation
        failures or unreadable input.
    """
    arguments = parse_arguments()
    try:
        text = arguments.prompt_file.read_text(encoding="utf-8")
    except OSError as error:
        print(f"ERROR: Cannot read {arguments.prompt_file}: {error}")
        return 1

    order, sections = parse_sections(text)
    errors = validate_structure(
        order=order,
        sections=sections,
        prompt4py=arguments.prompt4py,
        provided_variables=set(arguments.provided),
        text=text,
    )
    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALID")
    print("- Canonical headings, ordering, required content, and list fields passed.")
    if "_TIMESTAMP" in order:
        print("- Prompt4Py framework timestamp accepted.")
    if arguments.provided:
        print("- Declared runtime placeholders are complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
