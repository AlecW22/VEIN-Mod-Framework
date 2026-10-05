import json
import tempfile
import unittest
from pathlib import Path

from Framework.Bridge.export_plan import (
    build_load_plan,
    export_load_plan,
)
from Framework.Bridge.ue4ss_layout import (
    detect_ue4ss_layout,
    validate_ue4ss_layout,
)


class FakeResolutionResult:
    def __init__(self):
        self.load_order = ["core", "addon"]
        self.disabled = {
            "broken": "Missing required dependency"
        }
        self.errors = []


class BridgeTests(unittest.TestCase):

    def test_build_load_plan(self):
        result = FakeResolutionResult()

        plan = build_load_plan(result)

        self.assertEqual(
            plan["frameworkVersion"],
            "0.2"
        )

        self.assertEqual(
            plan["loadOrder"],
            ["core", "addon"]
        )

        self.assertIn(
            "broken",
            plan["disabled"]
        )

    def test_export_load_plan(self):
        result = FakeResolutionResult()

        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "vein_load_plan.json"

            export_load_plan(
                result,
                output
            )

            self.assertTrue(
                output.exists()
            )

            with output.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            self.assertEqual(
                data["loadOrder"],
                ["core", "addon"]
            )

    def test_detect_ue4ss_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            layout = detect_ue4ss_layout(
                str(root)
            )

            self.assertEqual(
                layout.win64_dir,
                root / "Vein" / "Binaries" / "Win64"
            )

            self.assertEqual(
                layout.ue4ss_mods_dir,
                root
                / "Vein"
                / "Binaries"
                / "Win64"
                / "ue4ss"
                / "Mods"
            )

    def test_validate_existing_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            mods = (
                root
                / "Vein"
                / "Binaries"
                / "Win64"
                / "ue4ss"
                / "Mods"
            )

            mods.mkdir(
                parents=True
            )

            layout = detect_ue4ss_layout(
                str(root)
            )

            checks = validate_ue4ss_layout(
                layout
            )

            self.assertTrue(
                checks["game_root"]
            )

            self.assertTrue(
                checks["ue4ss_mods_dir"]
            )


if __name__ == "__main__":
    unittest.main()