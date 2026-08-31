import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

module_path = ROOT / "3D_height_V11.py"
spec = importlib.util.spec_from_file_location("three_d_height_v11", module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_rt_suffixes_are_classified_as_coldbox_rt():
    assert module.ClassifyMeasurementType("RT +30") == "coldbox_rt"
    assert module.ClassifyMeasurementType("RT +40") == "coldbox_rt"
    assert module.ClassifyMeasurementType("RT +45") == "coldbox_rt"


def test_cold_suffixes_without_rt_stay_coldbox_cold():
    assert module.ClassifyMeasurementType("Cold +30") == "coldbox_cold"
