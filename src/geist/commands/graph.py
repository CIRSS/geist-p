import click
from geist.commands.cli import cli

@cli.group()
def graph():
    """Visualize a dataset"""
    pass

@graph.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be visualized (default "kb")')
@click.option('--rankdir', '-r', default='TB', type=click.Choice(['TB', 'BT', 'LR', 'RL']), help='Direction of the graph (default TB): TB or BT or LR or RL')
@click.option('--mappings', '-m', default=None, help='File of the mappings to shorten text (str): path of a JSON file, where the key is the original text and the value is the shorter text.')
@click.option('--on', '-on', default=None, help='Column(s) to be mapped.')
@click.option('--samecolor', '-sc', is_flag=True, default=True, help='Use the same color for same edges.')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the graph (default: current directory). If the given path (i.e., --outputfile) is a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default='res', type=str, help='Path of the file without extension to store the graph (default: res)')
@click.option('outputformats', '--outputformat', '-oformat', default=['none'], type=click.Choice(['none', 'svg', 'png', 'gv']), multiple=True, help='Format of the graph (default: none): none or svg or png or gv')
def rdflib(dataset, rankdir, mappings, on, samecolor, outputroot, outputfile, outputformats):
    """Visualize an RDF dataset"""    
    from geist.datastore.rdflib import rdflib_graph
    rdflib_graph(dataset, rankdir, mappings, on, samecolor, outputroot, outputfile, outputformats)
