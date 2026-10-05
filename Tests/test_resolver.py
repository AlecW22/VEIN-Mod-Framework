import unittest

from Framework.Core.manifest import ModManifest
from Framework.Core.resolver import resolve_load_order


def make_mod(
    mod_id,
    dependencies=None,
    load_before=None,
    load_after=None,
    conflicts=None,
):
    manifest = ModManifest(
        id=mod_id,
        name=mod_id,
        author="Test",
        version="1.0.0",
        description="Test mod",
        gameVersion="*",
        frameworkVersion=">=0.1",
        dependencies=dependencies or [],
        optionalDependencies=[],
        loadBefore=load_before or [],
        loadAfter=load_after or [],
        conflicts=conflicts or [],
        entryPoint="main.lua",
    )

    return {
        "manifest": manifest,
        "path": None,
    }


class ResolverTests(unittest.TestCase):

    def test_dependency_load_order(self):
        mods = {
            "core": make_mod("core"),
            "addon": make_mod(
                "addon",
                dependencies=["core"]
            ),
        }

        result = resolve_load_order(mods)

        self.assertEqual(
            result.load_order,
            ["core", "addon"]
        )

    def test_missing_dependency_disables_mod(self):
        mods = {
            "addon": make_mod(
                "addon",
                dependencies=["missing"]
            )
        }

        result = resolve_load_order(mods)

        self.assertIn(
            "addon",
            result.disabled
        )

    def test_alphabetical_fallback(self):
        mods = {
            "zebra": make_mod("zebra"),
            "alpha": make_mod("alpha"),
        }

        result = resolve_load_order(mods)

        self.assertEqual(
            result.load_order,
            ["alpha", "zebra"]
        )

    def test_cycle_detection(self):
        mods = {
            "a": make_mod(
                "a",
                load_after=["b"]
            ),
            "b": make_mod(
                "b",
                load_after=["a"]
            ),
        }

        result = resolve_load_order(mods)

        self.assertTrue(result.errors)
        self.assertIn("a", result.disabled)
        self.assertIn("b", result.disabled)


if __name__ == "__main__":
    unittest.main()