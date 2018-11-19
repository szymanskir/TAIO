import functools
import json
import logging
import os
import pandas as pd
import timeit
import random


from itertools import combinations_with_replacement
from typing import NamedTuple, Callable

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
    g2_type: str

    def get_test_case(self):
        logging.info('Generating test case...')
        graph_test_case = (generate_test_case(self.g1_type,
                                              self.n_g1_vertices,
                                              self.g1_density),
                           generate_test_case(self.g2_type,
                                              self.n_g2_vertices,
                                              self.g2_density))

        return graph_test_case


def measure_single_test_case(G1, G2, size_criterion, fun: Callable):
    logging.info(f'Measuring test case for {size_criterion}...')
    timer = timeit.Timer(functools.partial(fun, G1, G2, size_criterion))
    return round(timer.timeit(1), 3)


def measure_test_cases(test_cases,
                       fun: Callable,
                       size_criterion):
    return [measure_single_test_case(G1, G2, size_criterion, fun)
            for G1, G2 in test_cases]


def exact_algorithm_complexity_estimation():
    fixed_vertex_number = 8
    vertex_range = range(1, 3)

    sizes = [(fixed_vertex_number, x) for x in vertex_range]

    test_cases_parameters = [ParametrizedTestCase(size_pair[0], 0.5, 'random',
                                                  size_pair[1], 0.5, 'random')
                             for size_pair in sizes] 
    test_cases = [test_case_params.get_test_case()
                  for test_case_params in test_cases_parameters]

    exact_algorithm = find_mccis_factory(True)
    measurements_vertices = measure_test_cases(test_cases,
                                               exact_algorithm,
                                               'Vertices')
    measurements_vertices_and_edges = measure_test_cases(test_cases,
                                                         exact_algorithm,
                                                         'VerticesAndEdges')
    vertex_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        '|V2|': vertex_range
    })
    vertex_criterium_df.loc[:, '|V1|']=fixed_vertex_number


    vertex_and_edges_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        '|V2|': vertex_range
    })
    vertex_and_edges_criterium_df.loc[:, '|V1|']=fixed_vertex_number

    vertex_criterium_df.to_csv('results/exact-vertex-complexity-estimation.csv')
    vertex_and_edges_criterium_df.to_csv('results/exact-vertex-and-edges-complexity-estimation.csv')


def test_graph_pairing(graph_pair, size_range):
    # density does not matter in this case
    test_cases_parameters = [ParametrizedTestCase(size, 0.5, graph_pair[0],
                                                  size, 0.5, graph_pair[1])
                             for size in size_range] 

    test_cases = [test_case_params.get_test_case()
                  for test_case_params in test_cases_parameters]

    exact_algorithm = find_mccis_factory(True)
    measurements_vertices = measure_test_cases(test_cases,
                                               exact_algorithm,
                                               'Vertices')
    measurements_vertices_and_edges = measure_test_cases(test_cases,
                                                         exact_algorithm,
                                                         'VerticesAndEdges')

    vertex_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        'sizes': size_range 
    })


    vertex_and_edges_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        'sizes': size_range 
    })

    vertex_criterium_df.to_csv(f'results/{graph_pair[0]}-{graph_pair[1]}-vertex.csv')
    vertex_and_edges_criterium_df.to_csv('results/{graph_pair[0]}-{graph_pair[1]}-vertex-and-edges-complexity-estimation.csv')


def graph_type_factors():
    graph_types = {'path', 'tree', 'cycle', 'complete', 'bipartite'}
    graph_type_pairs = combinations_with_replacement(graph_types, 2)
    size_range = range(5, 6)

    [test_graph_pairing(pair, size_range)
     for pair in graph_type_pairs]


def density_factor():
    density_range = [x/10 for x in range(1, 10, 1)]
    fixed_size = 7
    test_cases_parameters = [ParametrizedTestCase(fixed_size, density, 'random',
                                                  fixed_size, density, 'random')
                             for density in density_range] 

    test_cases = [test_case_params.get_test_case()
                  for test_case_params in test_cases_parameters]

    exact_algorithm = find_mccis_factory(True)
    measurements_vertices = measure_test_cases(test_cases,
                                               exact_algorithm,
                                               'Vertices')
    measurements_vertices_and_edges = measure_test_cases(test_cases,
                                                         exact_algorithm,
                                                         'VerticesAndEdges')
    vertex_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        'gęstość': density_range
    })


    vertex_and_edges_criterium_df = pd.DataFrame({
        'czas obliczeń': measurements_vertices,
        'gęstość': density_range
    })

    vertex_criterium_df.to_csv('results/exact-vertex-density-factor.csv')
    vertex_and_edges_criterium_df.to_csv('results/exact-vertex-and-edges-density-factor.csv')


if __name__ == '__main__':
    random.seed(1)
    logging.basicConfig(level=logging.INFO)

    exact_algorithm_complexity_estimation()
    graph_type_factors()
    density_factor()
