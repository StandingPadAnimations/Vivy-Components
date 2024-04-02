from typing import cast
import unittest
from src import vivy_parse as vp
from src import vivy_types as vt
from . import data


class TestVivyParse(unittest.TestCase):
    def test_dict_to_vivy_data(self) -> None:
        self.assertIsNot(
            vp.dict_to_vivy_data(cast(vt.VIVY_JSON_TOP_LEVEL, data.DATA_JSON)), None
        )

    def test_load_vivy_json(self) -> None:
        with open(data.DATA_JSON_FILE, "r") as f:
            self.assertIsNot(vp.load_vivy_json(f), None)

    def test_open_vivy_json(self) -> None:
        from pathlib import Path

        path: Path = Path(data.DATA_JSON_FILE)
        self.assertIsNot(vp.open_vivy_json(path), None)


if __name__ == "__main__":
    unittest.main()
