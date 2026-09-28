from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import pandas as pd

import plotter_code_clean


def test_parse_xls_prints_surface_profile_and_returns_height_points():
    rows = [
        [None, None, "ExtractedSurfacePoints", "Surface Profile", "0.000", "0.291", "1.000"],
        [None, None, "Flatness1", "X", None, "10.0", None],
        [None, None, "Flatness1", "Y", None, "20.0", None],
        [None, None, "Flatness1", "Z", None, "0.5", None],
    ]
    output = StringIO()

    with patch.object(plotter_code_clean.pd, "read_excel", return_value=pd.DataFrame(rows)):
        with redirect_stdout(output):
            heightlist = plotter_code_clean.Parse_XLS("survey.xls", ".")

    assert "Surface Profile: 0.291" in output.getvalue()
    assert heightlist == [
        ["Flatness1", "X", "10.0", "Flatness1"],
        ["Flatness1", "Y", "20.0", "Flatness1"],
        ["Flatness1", "Z", "0.5", "Flatness1"],
    ]


def test_parse_xls_can_return_surface_profile_for_plot_annotation():
    rows = [
        [None, None, "ExtractedSurfacePoints", "Surface Profile", "0.000", "0.291", "1.000"],
        [None, None, "Flatness1", "X", None, "10.0", None],
        [None, None, "Flatness1", "Y", None, "20.0", None],
        [None, None, "Flatness1", "Z", None, "0.5", None],
    ]

    with patch.object(plotter_code_clean.pd, "read_excel", return_value=pd.DataFrame(rows)):
        heightlist, surface_profile = plotter_code_clean.Parse_XLS(
            "survey.xls", ".", return_surface_profile=True
        )

    assert surface_profile == "0.291"
    assert plotter_code_clean._format_flatness_label(surface_profile, surface_profile) == "Flatness = 0.291"
    assert plotter_code_clean._format_flatness_label(
        "0.299", "0.299", "module InColdbox -20 Cycle 10.xls", "module InColdbox -20 Cycle 10.xls"
    ) == "Flatness (Cold_10): 0.299"
    assert plotter_code_clean._format_flatness_label(
        "0.299", "0.299", "module InColdbox RT Cycle 10.xls", "module InColdbox RT Cycle 10.xls"
    ) == "Flatness (RT_10): 0.299"
    assert plotter_code_clean._format_flatness_label(
        "0.291", "0.299", "module InColdbox -20 Cycle 10.xls", "module InColdbox RT Cycle 10.xls"
    ) == "Flatness: Cold_10 - RT_10: 0.291 - 0.299 (mm)"
    assert plotter_code_clean._format_flatness_label(
        "0.299", "0.291", "module InColdbox RT Cycle 10.xls", "module InColdbox -20 Cycle 10.xls"
    ) == "Flatness: RT_10 - Cold_10: 0.299 - 0.291 (mm)"
    assert plotter_code_clean._format_flatness_label(
        "0.291", "0.299", "module InColdbox RT Cycle 10.xls", "module InColdbox RT Cycle 0.xls"
    ) == "Flatness: RT_10 - RT_0: 0.291 - 0.299 (mm)"
    assert len(heightlist) == 3