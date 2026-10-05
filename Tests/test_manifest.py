import unittest

from Framework.Core.manifest import ModManifest


class ManifestTests(unittest.TestCase):

    def test_valid_manifest(self):
        data = {
            "id": "example",
            "name": "Example Mod",
            "author": "Tester",
            "version": "1.0.0",
            "description": "Example",
            "gameVersion": "*",
            "frameworkVersion": ">=0.1",
            "dependencies": [],
            "optionalDependencies": [],
            "loadBefore": [],
            "loadAfter": [],
            "conflicts": [],
            "entryPoint": "main.lua",
        }

        manifest = ModManifest.from_dict(data)

        self.assertEqual(manifest.id, "example")
        self.assertEqual(manifest.name, "Example Mod")

    def test_missing_required_field(self):
        data = {
            "id": "broken"
        }

        with self.assertRaises(ValueError):
            ModManifest.from_dict(data)


if __name__ == "__main__":
    unittest.main()