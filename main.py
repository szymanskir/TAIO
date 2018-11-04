import logging
import click
from src.algorithms import find_mccis


@click.command()
@click.argument('graph_csv1', type=click.Path())
@click.argument('graph_csv2', type=click.Path())
@click.argument('output_file', type=click.Path())
@click.option('--size_criterion', type=click.Choice(['Vertices',
                                                     'VerticesAndEdges']))
@click.option('--exact/--approx', default=True)
@click.option('--visualize', is_flag=True)
def main(graph_csv1, graph_csv2, output_file, size_criterion, exact, visualize):
    find_mccis(graph_csv1, graph_csv2, output_file, size_criterion, exact, visualize)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
