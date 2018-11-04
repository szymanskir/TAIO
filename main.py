import click
from src.utils import read_graph, save_mccis
from src.algorithms import find_exact_mccis


@click.command()
@click.argument('graph_csv1', type=click.Path(),
                help="Path to the csv file containing data about the first graph.")
@click.argument('graph_csv2', type=click.Path(),
                help="Path to the csv file containing data about the second graph.")
@click.argument('output_file', type=click.Path(),
                help="Path to a file in which the result should be saved.")
@click.option('--size_criterion', type=str)
@click.option('--exact/--approx', default=True)
def main(graph_csv1, graph_csv2, size_criterion, output_file):
    graph1 = read_graph(graph_csv1)
    graph2 = read_graph(graph_csv2)

    mccis = find_exact_mccis(graph1, graph2, size_criterion)
    save_mccis(output_file, mccis.vertices)


if __name__ == '__main__':
    main()
