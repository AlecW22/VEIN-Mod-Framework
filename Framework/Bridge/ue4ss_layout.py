from dataclasses import dataclass
from pathlib import Path


@dataclass
class UE4SSLayout:
    game_root: Path
    binaries_dir: Path
    win64_dir: Path
    ue4ss_dir: Path
    ue4ss_mods_dir: Path


def detect_ue4ss_layout(game_root: str) -> UE4SSLayout:
    root = Path(game_root).expanduser().resolve()

    binaries_dir = root / "Vein" / "Binaries"
    win64_dir = binaries_dir / "Win64"
    ue4ss_dir = win64_dir / "ue4ss"
    ue4ss_mods_dir = ue4ss_dir / "Mods"

    return UE4SSLayout(
        game_root=root,
        binaries_dir=binaries_dir,
        win64_dir=win64_dir,
        ue4ss_dir=ue4ss_dir,
        ue4ss_mods_dir=ue4ss_mods_dir,
    )


def validate_ue4ss_layout(layout: UE4SSLayout):
    checks = {
        "game_root": layout.game_root.exists(),
        "binaries_dir": layout.binaries_dir.exists(),
        "win64_dir": layout.win64_dir.exists(),
        "ue4ss_dir": layout.ue4ss_dir.exists(),
        "ue4ss_mods_dir": layout.ue4ss_mods_dir.exists(),
    }

    return checks