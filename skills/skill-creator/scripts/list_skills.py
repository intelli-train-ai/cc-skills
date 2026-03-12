#!/usr/bin/env python3
"""List all plugins and skills from marketplace.json."""

import argparse
import json
import sys
from pathlib import Path

from scripts.utils import find_marketplace_json, list_marketplace_skills


def main():
    parser = argparse.ArgumentParser(description="List plugins and skills from marketplace.json")
    parser.add_argument("--plugin", default=None, help="Filter by plugin name")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Output as JSON")
    args = parser.parse_args()

    marketplace_path = find_marketplace_json()
    if not marketplace_path:
        print("Error: marketplace.json not found. Are you in a plugin repository?", file=sys.stderr)
        sys.exit(1)

    all_skills = list_marketplace_skills(marketplace_path)
    if args.plugin:
        all_skills = [s for s in all_skills if s["plugin_name"] == args.plugin]

    if not all_skills:
        print("No skills found.", file=sys.stderr)
        sys.exit(1)

    if args.as_json:
        output = [
            {
                "plugin": s["plugin_name"],
                "skill": s["skill_name"],
                "description": s["skill_description"],
                "path": str(s["skill_path"]),
            }
            for s in all_skills
        ]
        print(json.dumps(output, indent=2))
    else:
        current_plugin = None
        for s in all_skills:
            if s["plugin_name"] != current_plugin:
                current_plugin = s["plugin_name"]
                print(f"\n[{current_plugin}]")
            desc = s["skill_description"][:60] + "..." if len(s["skill_description"]) > 60 else s["skill_description"]
            print(f"  {s['skill_name']:30s} {desc}")


if __name__ == "__main__":
    main()
