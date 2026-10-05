import json
import tempfile
import unittest
from pathlib import Path

from Framework.Core.scanner import scan_mods


def valid_manifest(mod_id):
    return {
        "id": mod_id,
        "name": mod_id,
        "author": "Test",
        "version": "1.0.0",
        "description": "Test mod",
        "gameVersion": "*",
        "frameworkVersion": ">=0.1",
        "dependencies": [],
        "optionalDependencies": [],
        "loadBefore": [],
        "loadAfter": [],
        "conflicts": [],
        "entryPoint": "main.lua",
    }


class ScannerTests(unittest.TestCase):

    def test_scans_nested_mod(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            mod_dir = root / "Nested" / "Example"
            mod_dir.mkdir(parents=True)

            with (mod_dir / "mod.json").open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(valid_manifest("example"), file)

            result = scan_mods(str(root))

            self.assertIn("example", result.mods)
            self.assertFalse(result.errors)

    def test_malformed_json(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            mod_dir = root / "Broken"
            mod_dir.mkdir()

            with (mod_dir / "mod.json").open(
                "w",
                encoding="utf-8"
            ) as file:
                file.write("{ broken json")

            result = scan_mods(str(root))

            self.assertTrue(result.errors)

    def test_duplicate_mod_ids(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            for folder in ["A", "B"]:
                mod_dir = root / folder
                mod_dir.mkdir()

                with (mod_dir / "mod.json").open(
                    "w",
                    encoding="utf-8"
                ) as file:
                    json.dump(
                        valid_manifest("duplicate"),
                        file
                    )

            result = scan_mods(str(root))

            self.assertIn("duplicate", result.mods)
            self.assertTrue(
                any(
                    "Duplicate mod ID" in error
                    for error in result.errors
                )
            )


if __name__ == "__main__":
    unittest.main()