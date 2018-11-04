import pytest
import numpy as np

from numpy.testing import assert_array_equal

from src.algorithms import find_mccis


def assert_mccis_results(output_file, expected_output_file):
    output = np.loadtxt(output_file, delimiter=',').astype(int)
    expected_output = np.loadtxt(expected_output_file,
                                 delimiter=',').astype(int)
    assert_array_equal(output, expected_output)


def assert_find_mccis(G1,
                      G2,
                      tmp_path,
                      size_criterion,
                      exact,
                      expected):
    directory = tmp_path / "sub"
    directory.mkdir()
    output_file = directory / "output.csv"
    find_mccis(G1, G2, output_file, size_criterion, exact)

    assert_mccis_results(output_file, expected)


@pytest.mark.parametrize("G1, G2, expected", [
    ('data/2a.csv', 'data/2b.csv', 'data/2-correct.csv')
])
def test_exact_vertices_mccis(G1, G2, tmp_path, expected):
    assert_find_mccis(G1, G2, tmp_path, 'Vertices', True, expected)
