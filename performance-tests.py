import networkx as nx
import timeit, functools

from random import random
from itertools import combinations
from typing import NamedTuple, List, Callable

from src.algorithms import find_mccis_factory


class TestCase(NamedTuple):
    n_g1_vertices: int
    g1_density: float
    n_g2_vertices: int
    g2_density: float


def create_test_case(test_case: TestCase):
    G1 = create_test_graph(test_case.n_g1_vertices, test_case.g1_density)
    G2 = create_test_graph(test_case.n_g2_vertices, test_case.g2_density)

    return G1, G2


def create_test_graph(n_vertices: int, density: float):
    graph = nx.Graph()
    vertices = list(range(0, n_vertices))

    for i in range(0, n_vertices):
        graph.add_node(i)

    for x, y in combinations(vertices, 2):
        if random() < density:
            graph.add_edge(x, y)

    return graph


def measure_test_cases(test_cases: List[TestCase],
                       fun: Callable,
                       size_criterion):
    def measure_single_test_case(test_case: TestCase, size_criterion):
        G1, G2 = create_test_case(test_case)
        timer = timeit.Timer(functools.partial(fun, G1, G2, size_criterion))

        return timer.timeit(1)

    return [measure_single_test_case(test_case, size_criterion)
            for test_case in test_cases]


test_cases = [
    TestCase(14, 0.5, 14, 0.5)
]

find_mccis_exact = find_mccis_factory(exact=True)
find_mccis_approx = find_mccis_factory(exact=True)

print(measure_test_cases(test_cases, find_mccis_exact, 'Vertices'))
