#!/usr/bin/env python3
"""
Script to update Ansible role and collection versions in requirements.yml.
"""

import re

import requests
from packaging.version import parse as parse_version
from ruamel.yaml import YAML

YAML_PARSER = YAML()
YAML_PARSER.preserve_quotes = True
YAML_PARSER.explicit_start = True
YAML_PARSER.indent(mapping=2, sequence=4, offset=2)

with open("requirements.yml", encoding="utf-8") as f:
    REQUIREMENTS = YAML_PARSER.load(f)


def _get_role_latest_version(json_data):
    results = json_data.get("results", [])
    if not results:
        print(...)
        return None
    versions = results[0]["summary_fields"].get("versions", [])
    if not versions:
        print(...)
        return None
    return versions[0]["name"]


def _get_collection_latest_version(json_data):
    versions = json_data.get("data") or json_data.get("results")
    if not versions:
        print("⚠️ No versions found for collection.")
        return None

    highest = json_data.get("highest_version", {}).get("version")
    if highest:
        return highest

    try:
        sorted_versions = sorted(
            (v["version"] for v in versions if "version" in v),
            key=parse_version,
            reverse=True,
        )
        return sorted_versions[0] if sorted_versions else None
    except (TypeError, ValueError, KeyError) as error:
        print(f"⚠️ Error sorting versions: {error}")
        return None


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
        url = f"https://galaxy.ansible.com/api/v1/roles/?namespace={namespace}&name={name}"
    else:
        url = (
            f"https://galaxy.ansible.com"
            f"/api/v3/plugin/ansible/content/published"
            f"/collections/index/{namespace}/{name}/versions/"
        )

    try:
        resp = requests.get(url, timeout=10.0, headers={"Accept": "application/json"})
        resp.raise_for_status()
        json_data = resp.json()
    except (requests.RequestException, ValueError) as error:
        print(f"⚠️ Failed to fetch {item_type} '{namespace}.{name}': {error}")
        return None

    if item_type == "role":
        return _get_role_latest_version(json_data)
    return _get_collection_latest_version(json_data)


for entry in REQUIREMENTS.get("roles", []):
    if "name" in entry:
        match = re.match(r"([^\.]+)\.(.+)", entry["name"])
        if not match:
            continue
        ns, nm = match.groups()
        latest_version = get_latest_galaxy_version(ns, nm, "role")
        if latest_version and latest_version != entry["version"]:
            print(f"⬆️ Updating role {entry['name']} from {entry['version']} to {latest_version}")
            entry["version"] = latest_version

for entry in REQUIREMENTS.get("collections", []):
    if "name" in entry:
        ns, nm = entry["name"].split(".")
        latest_version = get_latest_galaxy_version(ns, nm, "collection")
        if latest_version and latest_version != entry["version"]:
            print(f"⬆️ Updating collection {entry['name']} from {entry['version']} to {latest_version}")
            entry["version"] = latest_version

with open("requirements.yml", "w", encoding="utf-8") as f:
    YAML_PARSER.dump(REQUIREMENTS, f)
