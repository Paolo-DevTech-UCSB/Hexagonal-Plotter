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


def test_thermal_pair_is_always_ordered_cold_then_rt():
    rt_file = "320MHF2WDSB0085 InColdbox RT Cycle 0.xls"
    cold_file = "320MHF2WDSB0085 InColdbox -20 Cycle 0.xls"

    assert module.OrderThermalPair(rt_file, cold_file) == (cold_file, rt_file)
    assert module.OrderThermalPair(cold_file, rt_file) == (cold_file, rt_file)


def test_cycle_parse_uses_cycle_number_not_module_serial_number():
    rt_file = "320MHF2WDSB0085 InColdbox RT Cycle 0.xls"
    cold_file = "320MHF2WDSB0085 InColdbox -20 Cycle 0.xls"

    assert module.CycleParse(rt_file) == 0
    assert module.CycleParse(cold_file) == 0
    assert module.BuildPlotFileName(
        rt_file, cold_file, "320MHF2WDSB0085", False
    ) == "320MHF2WDSB0085_RT_0_vs_Cold_0.png"


def test_cycle_parse_preserves_again_cycle_labels():
    assert module.CycleParse("module Cycle 100 again.xls") == 101
    assert module.CycleParse("module Cycle -70 again.xls") == -71
