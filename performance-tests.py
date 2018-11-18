import functools
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
    return timer.timeit(1)


def measure_test_cases(test_cases: List[TestCase],
                       fun: Callable,
                       size_criterion):
    graph_test_cases = [test_case.get_test_case() for test_case in test_cases]
    return [measure_single_test_case(G1, G2, size_criterion, fun)
            for G1, G2 in graph_test_cases]


def create_test_cases():
    logging.info('Preparing test cases...')
    sizes = [5, 6, 7]
    graph_types = ['path', 'complete', 'random']
    density = 0.8
    
    test_cases = list()
    for size in sizes:
        for x, y in combinations_with_replacement(graph_types, 2):
           test_cases.append(ParametrizedTestCase(
               size,
               density,
               x,
               size,
               density,
               y
           )) 

    return test_cases
    

random.seed(1)
logging.basicConfig(level=logging.INFO)

test_cases = create_test_cases()

find_mccis_exact = find_mccis_factory(exact=True)
find_mccis_approx = find_mccis_factory(exact=True)

print(measure_test_cases(test_cases, find_mccis_exact, 'Vertices'))
