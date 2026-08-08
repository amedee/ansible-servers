#!/usr/bin/env python3
"""Discover Molecule scenarios and generate Molecule coverage information."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess

COVERAGE_START = "<!-- molecule-coverage:start -->"
COVERAGE_END = "<!-- molecule-coverage:end -->"


def discover_roles() -> list[str]:
    """Return all Ansible role names."""
    roles_directory = pathlib.Path("roles")

    return sorted(path.name for path in roles_directory.iterdir() if path.is_dir())


def discover_scenarios() -> list[dict[str, str]]:
    """Return all discovered Molecule scenarios."""
    scenarios = []

    for molecule_file in sorted(pathlib.Path("roles").glob("*/molecule/*/molecule.yml")):
        scenario_directory = molecule_file.parent
        role_directory = scenario_directory.parent.parent

        scenarios.append(
            {
                "role": role_directory.name,
                "scenario": scenario_directory.name,
                "path": str(scenario_directory),
            }
        )

    return scenarios


def write_output(path: str, roles: list[str], scenarios: list[dict[str, str]]) -> None:
    """Write discovery results to GITHUB_OUTPUT."""
    with pathlib.Path(path).open("a", encoding="utf-8") as output:
        output.write(f"roles={json.dumps(roles, separators=(',', ':'))}\n")
        output.write(f"scenarios={json.dumps(scenarios, separators=(',', ':'))}\n")


def write_discovery_summary(
    path: str,
    roles: list[str],
    scenarios: list[dict[str, str]],
) -> None:
    """Write the discovery information to the GitHub step summary."""
    repository_name = os.environ["GITHUB_REPOSITORY"]
    sha = os.environ["GITHUB_SHA"]
    server = os.environ["GITHUB_SERVER_URL"]

    with pathlib.Path(path).open("a", encoding="utf-8") as summary:
        summary.write("### Discovered roles\n\n")

        for role in roles:
            summary.write(f"- `{role}`\n")

        summary.write("\n### Discovered scenarios\n\n")
        summary.write("| Role | Scenario | Path |\n")
        summary.write("| --- | --- | --- |\n")

        for scenario in scenarios:
            scenario_path = scenario["path"]
            scenario_url = f"{server}/{repository_name}/tree/{sha}/{scenario_path}"

            summary.write(
                f"| `{scenario['role']}` | `{scenario['scenario']}` | [`{scenario_path}`]({scenario_url}) |\n"
            )


def calculate_coverage(
    roles: list[str],
    scenarios: list[dict[str, str]],
) -> tuple[int, int, int]:
    """Return covered roles, total roles and percentage."""
    covered_roles = {scenario["role"] for scenario in scenarios}
    tested = len(covered_roles)
    total = len(roles)

    percentage = round(tested * 100 / total) if total else 0

    return tested, total, percentage


def coverage_color(percentage: int) -> str:
    """Return the shields.io color for a coverage percentage."""
    if percentage >= 90:
        return "brightgreen"

    if percentage >= 75:
        return "green"

    if percentage >= 50:
        return "yellow"

    if percentage >= 25:
        return "orange"

    return "red"


def render_coverage(
    roles: list[str],
    scenarios: list[dict[str, str]],
) -> str:
    """Render the Molecule coverage section."""
    tested, total, percentage = calculate_coverage(roles, scenarios)
    covered_roles = {scenario["role"] for scenario in scenarios}

    lines = [
        COVERAGE_START,
        f"## Molecule Coverage ({tested}/{total})",
        "",
        "| Role | Molecule |",
        "| --- | :---: |",
    ]

    for role in roles:
        role_url = f"https://github.com/{repository()}/tree/main/roles/{role}"

        molecule = "✅" if role in covered_roles else "❌"
        lines.append(f"| [`{role}`]({role_url}) | {molecule} |")

    lines.extend(
        [
            "",
            f"**{tested}/{total} roles ({percentage}%)**",
            COVERAGE_END,
        ]
    )

    return "\n".join(lines)


def repository() -> str:
    """Return the current GitHub repository."""
    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        check=True,
        capture_output=True,
        text=True,
    )

    remote = result.stdout.strip()

    if remote.endswith(".git"):
        remote = remote[:-4]

    if remote.startswith("git@github.com:"):
        return remote.removeprefix("git@github.com:")

    return remote.removeprefix("https://github.com/")


def update_readme(path: str, coverage: str) -> None:
    """Replace or append the Molecule coverage section."""
    readme_path = pathlib.Path(path)
    contents = readme_path.read_text(encoding="utf-8")

    start = contents.find(COVERAGE_START)
    end = contents.find(COVERAGE_END)

    if 0 <= start <= end and end >= 0:
        end += len(COVERAGE_END)
        contents = contents[:start] + coverage + contents[end:]
    else:
        separator = "" if contents.endswith("\n\n") else "\n\n"
        contents = contents.rstrip() + separator + coverage + "\n"

    readme_path.write_text(contents, encoding="utf-8")


def write_badge(
    directory: str,
    tested: int,
    total: int,
    percentage: int,
) -> None:
    """Generate the Shields-compatible badge JSON."""
    badge_directory = pathlib.Path(directory)
    badge_directory.mkdir(parents=True, exist_ok=True)

    badge = {
        "schemaVersion": 1,
        "label": "Molecule",
        "message": f"{tested}/{total} roles ({percentage}%)",
        "color": coverage_color(percentage),
    }

    (badge_directory / "molecule-coverage.json").write_text(
        json.dumps(badge, indent=2) + "\n",
        encoding="utf-8",
    )


def write_coverage_summary(path: str, coverage: str) -> None:
    """Write the coverage section to the GitHub step summary."""
    with pathlib.Path(path).open("a", encoding="utf-8") as summary:
        summary.write(coverage)
        summary.write("\n")


def discover_command(args: argparse.Namespace) -> None:
    """Handle the discovery command."""
    roles = discover_roles()
    scenarios = discover_scenarios()

    write_output(args.roles_output, roles, scenarios)
    write_discovery_summary(args.summary_output, roles, scenarios)


def coverage_command(args: argparse.Namespace) -> None:
    """Handle the coverage command."""
    roles: list[str] = json.loads(args.roles)
    scenarios: list[dict[str, str]] = json.loads(args.scenarios)

    tested, total, percentage = calculate_coverage(roles, scenarios)
    coverage = render_coverage(roles, scenarios)

    update_readme(args.readme, coverage)
    write_badge(args.badge_directory, tested, total, percentage)
    write_coverage_summary(args.summary_output, coverage)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description="Discover Molecule scenarios and calculate coverage.")

    subparsers = parser.add_subparsers(required=True)

    discover = subparsers.add_parser("discover")
    discover.add_argument("--roles-output", required=True)
    discover.add_argument("--summary-output", required=True)
    discover.set_defaults(func=discover_command)

    coverage = subparsers.add_parser("coverage")
    coverage.add_argument("--roles", required=True)
    coverage.add_argument("--scenarios", required=True)
    coverage.add_argument("--readme", required=True)
    coverage.add_argument("--badge-directory", required=True)
    coverage.add_argument("--summary-output", required=True)
    coverage.set_defaults(func=coverage_command)

    return parser


def main() -> None:
    """Run the command-line interface."""
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
