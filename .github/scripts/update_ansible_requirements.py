#!/usr/bin/env python3
"""
Script to update Ansible role and collection versions in requirements.yml.
"""

import re

import requests
from packaging.version import parse as parse_version
from ruamel.yaml import YAML

_yaml_parser = YAML()  # nosemgrep
_yaml_parser.preserve_quotes = True

with open("requirements.yml", encoding="utf-8") as f:
    _requirements = _yaml_parser.load(f)  # nosemgrep


def get_latest_galaxy_version(namespace, name, item_type):
    """
    Fetch the latest version of a role or collection from Ansible Galaxy.

    Args:
        namespace (str): Namespace or author name.
        name (str): Role or collection name.
        item_type (str): Either 'role' or 'collection'.

    Returns:
        str or None: Latest stable version string, or None if not found.
    """
    if item_type == "role":
        url = (
            f"https://galaxy.ansible.com/api/v1/roles/"
            f"?namespace={namespace}&name={name}"
        )
    else:
        url = (
            f"https://galaxy.ansible.com"
            f"/api/v3/plugin/ansible/content/published"
            f"/collections/index/{namespace}/{name}/versions/"
        )

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        json_data = resp.json()
    except (requests.RequestException, ValueError) as e:
        print(f"⚠️ Failed to fetch {item_type} '{namespace}.{name}': {e}")
        return None

    if item_type == "role":
        results = json_data.get("results", [])
        if not results:
            print(f"⚠️ No role found for {namespace}.{name}")
            return None
        versions = results[0]["summary_fields"].get("versions", [])
        if not versions:
            print(f"⚠️ No versions found for role {namespace}.{name}")
            return None
        return versions[0]["name"]

    # collection case
    versions = json_data.get("data") or json_data.get("results")
    if not versions:
        print(f"⚠️ No versions for collection {namespace}.{name}")
        return None

    highest = json_data.get("highest_version", {}).get("version")
    if highest:
        return highest

    # fallback: sort versions by parsed version and return highest
    return sorted(
        (v["version"] for v in versions),
        key=parse_version,
        reverse=True,
    )[0]


for entry in _requirements.get("roles", []):
    if "name" in entry:
        match = re.match(r"([^\.]+)\.(.+)", entry["name"])
        if not match:
            continue
        ns, nm = match.groups()
        latest_version = get_latest_galaxy_version(ns, nm, "role")
        if latest_version and latest_version != entry["version"]:
            print(
                f"⬆️ Updating role {entry['name']} from {entry['version']} to {latest_version}"
            )
            entry["version"] = latest_version

for entry in _requirements.get("collections", []):
    if "name" in entry:
        ns, nm = entry["name"].split(".")
        latest_version = get_latest_galaxy_version(ns, nm, "collection")
        if latest_version and latest_version != entry["version"]:
            print(
                f"⬆️ Updating collection {entry['name']} from {entry['version']} to {latest_version}"
            )
            entry["version"] = latest_version

with open("requirements.yml", "w", encoding="utf-8") as f:
    _yaml_parser.dump(_requirements, f)
