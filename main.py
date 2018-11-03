import click
from src.utils import read_graph
from src.algorithms import find_exact_mccis


@click.command()
@click.argument('graph_csv1', type=click.Path())
@click.argument('graph_csv2', type=click.Path())
def main(graph_csv1, graph_csv2):
    graph1 = read_graph(graph_csv1)
    graph2 = read_graph(graph_csv2)

    mcis = find_exact_mccis(graph1, graph2)
    print(mcis)


if __name__ == '__main__':
    main()
