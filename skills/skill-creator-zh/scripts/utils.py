"""Shared utilities for skill-creator scripts."""

import json
import sys
from pathlib import Path


def parse_skill_md(skill_path: Path) -> tuple[str, str, str]:
    """Parse a SKILL.md file, returning (name, description, full_content)."""
    content = (skill_path / "SKILL.md").read_text()
    lines = content.split("\n")

    if lines[0].strip() != "---":
        raise ValueError("SKILL.md missing frontmatter (no opening ---)")

    end_idx = None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        raise ValueError("SKILL.md missing frontmatter (no closing ---)")

    name = ""
    description = ""
    frontmatter_lines = lines[1:end_idx]
    i = 0
    while i < len(frontmatter_lines):
        line = frontmatter_lines[i]
        if line.startswith("name:"):
            name = line[len("name:"):].strip().strip('"').strip("'")
        elif line.startswith("description:"):
            value = line[len("description:"):].strip()
            # Handle YAML multiline indicators (>, |, >-, |-)
            if value in (">", "|", ">-", "|-"):
                continuation_lines: list[str] = []
                i += 1
                while i < len(frontmatter_lines) and (frontmatter_lines[i].startswith("  ") or frontmatter_lines[i].startswith("\t")):
                    continuation_lines.append(frontmatter_lines[i].strip())
                    i += 1
                description = " ".join(continuation_lines)
                continue
            else:
                description = value.strip('"').strip("'")
        i += 1

    return name, description, content


def find_marketplace_json(start_path: Path | None = None) -> Path | None:
    """Find .claude-plugin/marketplace.json by walking up from start_path."""
    current = (start_path or Path.cwd()).resolve()
    for parent in [current, *current.parents]:
        candidate = parent / ".claude-plugin" / "marketplace.json"
        if candidate.is_file():
            return candidate
    return None


def load_marketplace(marketplace_path: Path) -> dict:
    """Load and parse marketplace.json."""
    return json.loads(marketplace_path.read_text())


def list_marketplace_skills(marketplace_path: Path) -> list[dict]:
    """List all plugins and their skills from marketplace.json.

    Returns a list of dicts with keys: plugin_name, skill_path, skill_name.
    skill_name is parsed from the SKILL.md if it exists, otherwise derived from the directory name.
    """
    marketplace = load_marketplace(marketplace_path)
    repo_root = marketplace_path.parent.parent  # .claude-plugin/ is one level below root
    results = []

    for plugin in marketplace.get("plugins", []):
        plugin_name = plugin["name"]
        source = plugin.get("source", "./")
        for skill_rel in plugin.get("skills", []):
            skill_abs = (repo_root / source / skill_rel).resolve()
            skill_md = skill_abs / "SKILL.md"
            if skill_md.is_file():
                try:
                    name, description, _ = parse_skill_md(skill_abs)
                except ValueError:
                    name = skill_abs.name
                    description = ""
            else:
                name = skill_abs.name
                description = ""
            results.append({
                "plugin_name": plugin_name,
                "skill_path": skill_abs,
                "skill_name": name,
                "skill_description": description,
            })

    return results


def resolve_skills_from_marketplace(
    marketplace_path: Path,
    plugin_name: str | None = None,
    skill_name: str | None = None,
) -> list[dict]:
    """Resolve skill paths from marketplace.json, optionally filtered by plugin and/or skill name."""
    all_skills = list_marketplace_skills(marketplace_path)

    if plugin_name:
        all_skills = [s for s in all_skills if s["plugin_name"] == plugin_name]
    if skill_name:
        all_skills = [s for s in all_skills if s["skill_name"] == skill_name]

    return all_skills


def add_marketplace_args(parser):
    """Add --plugin and --skill-name arguments to an argparse parser as alternatives to --skill-path."""
    parser.add_argument("--skill-path", default=None, help="Path to skill directory (direct)")
    parser.add_argument("--plugin", default=None, help="Plugin name from marketplace.json (e.g. document-skills)")
    parser.add_argument("--skill-name", default=None, help="Skill name within a plugin (use with --plugin)")


def resolve_skill_path_from_args(args) -> Path:
    """Resolve a single skill path from args (either --skill-path or --plugin + --skill-name).

    Exits with error if resolution fails or returns multiple results without --skill-name.
    """
    if args.skill_path:
        skill_path = Path(args.skill_path)
        if not (skill_path / "SKILL.md").exists():
            print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
            sys.exit(1)
        return skill_path

    if not args.plugin:
        print("Error: Either --skill-path or --plugin is required.", file=sys.stderr)
        sys.exit(1)

    marketplace_path = find_marketplace_json()
    if not marketplace_path:
        print("Error: marketplace.json not found. Are you in a plugin repository?", file=sys.stderr)
        sys.exit(1)

    matches = resolve_skills_from_marketplace(marketplace_path, args.plugin, getattr(args, "skill_name", None))

    if not matches:
        print(f"Error: No skills found for plugin='{args.plugin}'"
              + (f", skill-name='{args.skill_name}'" if getattr(args, "skill_name", None) else ""),
              file=sys.stderr)
        sys.exit(1)

    if len(matches) > 1 and not getattr(args, "skill_name", None):
        print(f"Error: Plugin '{args.plugin}' contains {len(matches)} skills. Use --skill-name to select one:",
              file=sys.stderr)
        for s in matches:
            print(f"  - {s['skill_name']} ({s['skill_path']})", file=sys.stderr)
        sys.exit(1)

    return matches[0]["skill_path"]


def resolve_skill_paths_from_args(args) -> list[Path]:
    """Resolve one or more skill paths from args. Returns all skills in a plugin if --skill-name is not specified."""
    if args.skill_path:
        skill_path = Path(args.skill_path)
        if not (skill_path / "SKILL.md").exists():
            print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
            sys.exit(1)
        return [skill_path]

    if not args.plugin:
        print("Error: Either --skill-path or --plugin is required.", file=sys.stderr)
        sys.exit(1)

    marketplace_path = find_marketplace_json()
    if not marketplace_path:
        print("Error: marketplace.json not found. Are you in a plugin repository?", file=sys.stderr)
        sys.exit(1)

    matches = resolve_skills_from_marketplace(marketplace_path, args.plugin, getattr(args, "skill_name", None))

    if not matches:
        print(f"Error: No skills found for plugin='{args.plugin}'"
              + (f", skill-name='{args.skill_name}'" if getattr(args, "skill_name", None) else ""),
              file=sys.stderr)
        sys.exit(1)

    return [s["skill_path"] for s in matches]
