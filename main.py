import click
import logging
from src.utils import read_graph, save_mccis
from src.algorithms import find_mccis_factory


@click.command()
@click.argument('graph_csv1', type=click.Path())
@click.argument('graph_csv2', type=click.Path())
@click.argument('output_file', type=click.Path())
@click.option('--size_criterion', type=click.Choice(['Vertices',
                                                     'VerticesAndEdges']))
@click.option('--exact/--approx', default=True)
def main(graph_csv1, graph_csv2, output_file, size_criterion, exact):
    logger = logging.getLogger('main')

    logger.info(f'Reading data from {graph_csv1} and {graph_csv2}...')
    G1 = read_graph(graph_csv1)
    G2 = read_graph(graph_csv2)

    logger.info('Calculating maximal mccis...')
    find_mccis = find_mccis_factory(exact)
    mccis = find_mccis(G1, G2, size_criterion)

    logger.info(f'Saving results to {output_file}...')
    save_mccis(output_file, mccis.vertices)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
