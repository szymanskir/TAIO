import functools
import json
import logging
import networkx as nx
import timeit
import random

from itertools import combinations, combinations_with_replacement
from typing import NamedTuple, List, Callable

from src.algorithms import find_mccis_factory
from src.test_case_generator import generate_test_case


class TestCase():
    def get_test_case(self):
        raise Exception("TestCase.get_test_case always fails!")


class ParametrizedTestCase(TestCase, NamedTuple):
    n_g1_vertices: int
    g1_density: float
    g1_type: str
    n_g2_vertices: int
    g2_density: float
    g2_type:str

    def get_test_case(self):
        graph_test_case = (generate_test_case(self.g1_type,
                                              self.n_g1_vertices,
                                              self.g1_density),
                           generate_test_case(self.g2_type,
                                             self.n_g2_vertices,
                                             self.g2_density))
        return graph_test_case


def measure_single_test_case(G1, G2, size_criterion, fun: Callable):
    logging.info('Measuring test case...')
    timer = timeit.Timer(functools.partial(fun, G1, G2, size_criterion))
    return round(timer.timeit(1), 3)


def measure_test_cases(test_cases: List[TestCase],
                       fun: Callable,
                       size_criterion):
    graph_test_cases = [test_case.get_test_case() for test_case in test_cases]
    return [measure_single_test_case(G1, G2, size_criterion, fun)
            for G1, G2 in graph_test_cases]


def prepare_test_cases(graph_type1, graph_type2, sizes, density=None):
    logging.info(f'Preparing test cases for ({graph_type1}, {graph_type2})...')
    test_cases = [ParametrizedTestCase(size, density, graph_type1, size, density, graph_type2)
                  for size in sizes]

    return test_cases

if __name__ == '__main__':
    random.seed(1)
    logging.basicConfig(level=logging.INFO)

    sizes = [x for x in range(5, 6)]
    graph_types = {'path', 'complete', 'random', 'tree', 'cycle'}
    graph_type_pairs = combinations_with_replacement(graph_types, 2)
    density = 0.8

    test_cases = {str(pair): prepare_test_cases(*pair, sizes, density)
                  for pair in graph_type_pairs}

    find_mccis_exact = find_mccis_factory(exact=True)
    find_mccis_approx = find_mccis_factory(exact=True)

    logging.info('Starting performance tests...')
    results = {pair: dict(zip(sizes, measure_test_cases(test_cases[pair],
                                                        find_mccis_exact,
                                                        'Vertices')))
               for pair in test_cases}
    logging.info(f'Obtained result:\n {json.dumps(results, indent=4)}')
    
    with open('simulation_results.json', 'w') as outfile:
        json.dump(results, outfile, indent=4)
