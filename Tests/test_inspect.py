import tempfile
import unittest
from pathlib import Path

from Framework.Bridge.inspect import inspect_install


class InspectTests(unittest.TestCase):

    def test_complete_layout_returns_success(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)

            (
                root
                / "Vein"
                / "Binaries"
                / "Win64"
                / "ue4ss"
                / "Mods"
            ).mkdir(parents=True)

            result = inspect_install(str(root))

            self.assertEqual(result, 0)

    def test_missing_layout_returns_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            result = inspect_install(temp)

            self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()