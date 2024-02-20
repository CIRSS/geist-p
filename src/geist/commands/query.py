import click, sys
from geist.commands.cli import cli

@cli.group()
def query():
    """Perform a query on a dataset"""
    pass

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be queried (default "kb")')
@click.option('--file', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the SPARQL query to execute')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def rdflib(dataset, file, outputroot, outputfile):
    """Perform a SPARQL query on a dataset"""
    from geist.datastore.rdflib import rdflib_query
    rdflib_query(dataset, file, outputroot, outputfile)
