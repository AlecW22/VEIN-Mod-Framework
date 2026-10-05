from pathlib import Path

from .scanner import scan_mods
from .resolver import resolve_load_order
from .logger import build_report


def run(mods_directory="Mods"):
    scan_result = scan_mods(mods_directory)

    resolution_result = resolve_load_order(
        scan_result.mods
    )

    report = build_report(
        scan_result,
        resolution_result
    )

    print(report)

    return scan_result, resolution_result


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]
    mods_directory = project_root / "Mods"

    run(str(mods_directory))