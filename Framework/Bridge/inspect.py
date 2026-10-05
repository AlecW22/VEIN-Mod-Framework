import argparse

from .ue4ss_layout import (
    detect_ue4ss_layout,
    validate_ue4ss_layout,
)


def inspect_install(game_root):
    layout = detect_ue4ss_layout(game_root)
    checks = validate_ue4ss_layout(layout)

    print("[VEIN Mod Framework]")
    print("Bridge Inspector v0.2")
    print()

    print(f"Game root: {layout.game_root}")
    print()

    locations = [
        ("VEIN game root", layout.game_root, checks["game_root"]),
        ("Binaries", layout.binaries_dir, checks["binaries_dir"]),
        ("Win64", layout.win64_dir, checks["win64_dir"]),
        ("UE4SS", layout.ue4ss_dir, checks["ue4ss_dir"]),
        ("UE4SS Mods", layout.ue4ss_mods_dir, checks["ue4ss_mods_dir"]),
    ]

    for name, path, exists in locations:
        status = "FOUND" if exists else "MISSING"
        print(f"[{status}] {name}")
        print(f"         {path}")

    print()

    if all(checks.values()):
        print("VEIN + UE4SS layout appears ready.")
        return 0

    print("Installation is incomplete or UE4SS was not detected.")
    return 1


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a VEIN installation without modifying it."
    )

    parser.add_argument(
        "game_root",
        help="Path to the VEIN installation folder",
    )

    args = parser.parse_args()

    raise SystemExit(
        inspect_install(args.game_root)
    )


if __name__ == "__main__":
    main()