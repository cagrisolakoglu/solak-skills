#!/usr/bin/env python3
"""Structural validation for the solak-design-ui skill.

Run from anywhere:

    python skills/solak-design-ui/scripts/validate_skill.py

Standard library only, on purpose: this runs in CI and on a fresh checkout with
no install step. The manifest is a small, fixed YAML subset (nested maps and
lists of scalars), so it is parsed here rather than pulling in PyYAML.

Exit code 0 on success, 1 on any error. Warnings never fail the run.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SKILL_NAME = "solak-design-ui"
REQUIRED_TAGS = {"design", "ux", "frontend", "ui"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
VALID_STATUS = {"draft", "beta", "stable", "deprecated"}

errors: list[str] = []
warnings: list[str] = []


def error(msg: str) -> None:
    errors.append(msg)


def warn(msg: str) -> None:
    warnings.append(msg)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------- manifest --


def load_manifest(path: Path) -> dict:
    """Parse the manifest's YAML subset: nested maps, lists of scalars, comments.

    Anything outside that subset is a manifest authoring error, not something to
    tolerate silently — an unparsed key would make a check pass by being absent.
    """
    lines = []
    for raw in read(path).splitlines():
        if raw.lstrip().startswith("#"):
            continue
        line = raw.rstrip()
        if not line.strip():
            continue
        lines.append(line)

    def parse(index: int, indent: int):
        if index < len(lines) and lines[index].strip().startswith("- "):
            items: list[str] = []
            while index < len(lines):
                cur = lines[index]
                cur_indent = len(cur) - len(cur.lstrip())
                if cur_indent < indent or not cur.strip().startswith("- "):
                    break
                items.append(cur.strip()[2:].strip().strip("'\""))
                index += 1
            return items, index

        node: dict = {}
        while index < len(lines):
            cur = lines[index]
            cur_indent = len(cur) - len(cur.lstrip())
            if cur_indent < indent:
                break
            body = cur.strip()
            if ":" not in body:
                error(f"manifest.yaml: cannot parse line: {body}")
                index += 1
                continue
            key, _, value = body.partition(":")
            key, value = key.strip(), value.strip().strip("'\"")
            index += 1
            if value:
                node[key] = value
            else:
                child, index = parse(index, cur_indent + 1)
                node[key] = child
        return node, index

    parsed, _ = parse(0, 0)
    return parsed


def manifest_paths(manifest: dict) -> list[str]:
    """Every skill-relative path the manifest declares, in declaration order."""
    out: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, str) and item.endswith((".md", ".py", ".yaml")):
                    out.append(item)

    for key in ("required", "surface_routes", "cross_cutting", "evals", "examples"):
        walk(manifest.get(key))
    # Preserve order, drop repeats — routing intentionally lists files twice.
    return list(dict.fromkeys(out))


# ------------------------------------------------------------ front matter --


def parse_front_matter(text: str) -> dict[str, str]:
    """Flat key/value read of the SKILL.md front matter, including `metadata:`."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end == -1:
        return {}
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        if value:
            fields[key.strip()] = value
    return fields


# ------------------------------------------------------------------ checks --


def find_local_markdown_paths(text: str) -> set[str]:
    """Skill-local file references: backticked paths and Markdown links."""
    found = set(re.findall(r"`([A-Za-z0-9._/-]+\.md)`", text))
    for target in re.findall(r"\]\(([^)]+)\)", text):
        target = target.split("#", 1)[0].strip()
        if target.endswith(".md") and not target.startswith(("http://", "https://")):
            found.add(target)
    return found


def resolve(owner: Path, ref: str) -> Path | None:
    """A bare `tables.md` resolves against references/; a path resolves as given."""
    candidates = [owner.parent / ref, SKILL_DIR / ref]
    if "/" not in ref:
        candidates.append(SKILL_DIR / "references" / ref)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def validate_required_files(manifest: dict) -> int:
    checked = 0
    for rel in manifest_paths(manifest):
        checked += 1
        path = SKILL_DIR / rel
        if not path.is_file():
            error(f"{rel} is declared in manifest.yaml but does not exist")
        elif path.suffix == ".md" and not read(path).strip():
            error(f"{rel} is empty")
    return checked


def validate_no_retired_names(manifest: dict, md_files: list[Path]) -> None:
    for rel in manifest.get("retired_names") or []:
        if (SKILL_DIR / rel).exists():
            error(f"{rel} is a retired filename but exists on disk")
        name = Path(rel).name
        for path in md_files:
            if re.search(rf"(?<![A-Za-z0-9-]){re.escape(name)}", read(path)):
                error(f"{path.relative_to(SKILL_DIR).as_posix()} references retired name {name}")


def validate_references(md_files: list[Path]) -> int:
    checked = 0
    for path in md_files:
        rel = path.relative_to(SKILL_DIR).as_posix()
        for ref in sorted(find_local_markdown_paths(read(path))):
            checked += 1
            if ref.startswith("../") or ref.startswith("/"):
                error(f"{rel} links outside the skill directory: {ref}")
                continue
            if resolve(path, ref) is None:
                error(f"{rel} references {ref} but it does not exist")
    return checked


def headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.startswith("#")]


def has_section(text: str, *words: str) -> bool:
    lowered = [h.lower() for h in headings(text)]
    return any(any(w in h for w in words) for h in lowered)


def validate_required_sections(manifest: dict) -> None:
    for rel in manifest.get("required", {}).get("references") or []:
        path = SKILL_DIR / rel
        if not path.is_file():
            continue
        text = read(path)
        if not text.startswith("# "):
            error(f"{rel} has no top-level heading on line 1")
        if not has_section(text, "verification", "gate", "checklist"):
            error(f"{rel} has no verification or blocking-gates section")

    for rel in manifest.get("evals") or []:
        path = SKILL_DIR / rel
        if not path.is_file():
            continue
        text = read(path)
        if not has_section(text, "expected"):
            error(f"{rel} is missing an 'Expected' section")
        if not has_section(text, "forbidden", "must not"):
            error(f"{rel} is missing a 'Forbidden' section")
        if not has_section(text, "result"):
            error(f"{rel} is missing a 'Result' section")

    for rel in (manifest.get("examples") or {}).get("golden") or []:
        path = SKILL_DIR / rel
        if not path.is_file():
            continue
        text = read(path)
        if not has_section(text, "surface contract", "context"):
            error(f"{rel} has no surface contract or context section")
        if not has_section(text, "validation", "verification"):
            error(f"{rel} has no validation section")
        if not has_section(text, "risk"):
            error(f"{rel} does not state a remaining risk")

    for rel in (manifest.get("examples") or {}).get("anti_patterns") or []:
        path = SKILL_DIR / rel
        if not path.is_file():
            continue
        text = read(path)
        for needed, words in (
            ("Bad implementation", ("bad implementation",)),
            ("Why it fails", ("why it fails",)),
            ("Correct direction", ("correct direction",)),
            ("Detection checklist", ("detection",)),
        ):
            if not has_section(text, *words):
                error(f"{rel} is missing section: {needed}")


def validate_metadata(front: dict[str, str]) -> None:
    if not front:
        error("SKILL.md has no YAML front matter")
        return
    if front.get("name") != SKILL_NAME:
        error(f"SKILL.md name is {front.get('name')!r}, expected {SKILL_NAME!r}")
    if not front.get("description"):
        error("SKILL.md front matter has no description")
    version = front.get("version", "")
    if not SEMVER.match(version):
        error(f"SKILL.md version {version!r} is not valid semantic versioning")
    status = front.get("status", "")
    if status not in VALID_STATUS:
        error(f"SKILL.md status {status!r} is not one of {sorted(VALID_STATUS)}")
    tags = set(re.findall(r"[a-z0-9-]+", front.get("tags", "")))
    missing = REQUIRED_TAGS - tags
    if missing:
        error(f"SKILL.md is missing required tags: {sorted(missing)}")


def validate_consistency(manifest: dict, skill_text: str) -> None:
    if manifest.get("name") != SKILL_NAME:
        error(f"manifest.yaml name is {manifest.get('name')!r}, expected {SKILL_NAME!r}")

    front = parse_front_matter(skill_text)
    if front.get("status") and manifest.get("status") != front["status"]:
        error(
            f"status disagrees: manifest.yaml says {manifest.get('status')!r}, "
            f"SKILL.md says {front['status']!r}"
        )

    # Every reference the manifest requires should be reachable from SKILL.md,
    # directly or through another reference — an unreachable rule is a dead rule.
    corpus = skill_text
    for path in sorted((SKILL_DIR / "references").glob("*.md")):
        corpus += read(path)
    for rel in manifest.get("required", {}).get("references") or []:
        name = Path(rel).name
        occurrences = len(re.findall(re.escape(name), corpus))
        if occurrences <= 1:
            warn(f"{rel} is referenced nowhere but itself")

    # Routing in SKILL.md must name files that exist.
    for ref in sorted(find_local_markdown_paths(skill_text)):
        if resolve(SKILL_DIR / "SKILL.md", ref) is None:
            error(f"SKILL.md routing names {ref}, which does not exist")

    if "## Scope triage" not in skill_text:
        error("SKILL.md has no 'Scope triage' section")
    if "## Reference routing" not in skill_text:
        error("SKILL.md has no 'Reference routing' section")


# -------------------------------------------------------------------- main --


def main() -> int:
    manifest_path = SKILL_DIR / "manifest.yaml"
    skill_path = SKILL_DIR / "SKILL.md"

    if not skill_path.is_file():
        print("ERROR: SKILL.md does not exist", file=sys.stderr)
        return 1
    if not manifest_path.is_file():
        print("ERROR: manifest.yaml does not exist", file=sys.stderr)
        return 1

    manifest = load_manifest(manifest_path)
    skill_text = read(skill_path)
    md_files = sorted(
        p for p in SKILL_DIR.rglob("*.md") if ".git" not in p.parts
    )

    files_checked = validate_required_files(manifest) + 1
    validate_no_retired_names(manifest, md_files)
    refs_checked = validate_references(md_files)
    validate_required_sections(manifest)
    validate_metadata(parse_front_matter(skill_text))
    validate_consistency(manifest, skill_text)

    for path in md_files:
        if not read(path).strip():
            error(f"{path.relative_to(SKILL_DIR).as_posix()} is empty")

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}", file=sys.stderr)

    if errors:
        print(
            f"\n{SKILL_NAME} validation failed\n"
            f"Files checked: {files_checked}\n"
            f"References checked: {refs_checked}\n"
            f"Warnings: {len(warnings)}\n"
            f"Errors: {len(errors)}",
            file=sys.stderr,
        )
        return 1

    print(
        f"{SKILL_NAME} validation passed\n"
        f"Files checked: {files_checked}\n"
        f"References checked: {refs_checked}\n"
        f"Warnings: {len(warnings)}\n"
        f"Errors: 0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
