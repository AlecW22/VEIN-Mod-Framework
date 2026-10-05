import json
from pathlib import Path

from .manifest import ModManifest


class ScanResult:
    def __init__(self):
        self.mods = {}
        self.errors = []


def scan_mods(mods_directory: str) -> ScanResult:
    result = ScanResult()

    root = Path(mods_directory)

    if not root.exists():
        result.errors.append(
            f"Mods directory does not exist: {root}"
        )
        return result

    manifest_files = sorted(
        root.rglob("mod.json"),
        key=lambda p: str(p).lower()
    )

    for manifest_path in manifest_files:
        try:
            with manifest_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            manifest = ModManifest.from_dict(data)

            if manifest.id in result.mods:
                result.errors.append(
                    f"Duplicate mod ID '{manifest.id}' "
                    f"found in {manifest_path}"
                )
                continue

            result.mods[manifest.id] = {
                "manifest": manifest,
                "path": manifest_path.parent,
            }

        except json.JSONDecodeError as exc:
            result.errors.append(
                f"Malformed JSON in {manifest_path}: {exc}"
            )

        except (ValueError, TypeError) as exc:
            result.errors.append(
                f"Invalid manifest in {manifest_path}: {exc}"
            )

    return result