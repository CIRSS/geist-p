import click, sys
from geist.commands.cli import cli

@cli.group()
def load():
    """Import data into a dataset"""
    pass

@load.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to load a file (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
def rdflib(dataset, inputfile, inputformat, colnames):
    """Import data into a RDF dataset"""
    from geist.datastore.rdflib import rdflib_load
    rdflib_load(dataset, inputfile.read(), inputformat, colnames)

@load.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of SQL dataset to load a file (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as a table')
@click.option('--inputformat', '-iformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the file to be loaded as a table (default csv)')
@click.option('--table', '-t', required=True, type=str, help='Name of the table to be created')
def duckdb(dataset, inputfile, inputformat, table):
    """Import data into a SQL dataset"""
    from geist.datastore.duckdb import duckdb_load
    duckdb_load(dataset, inputfile.read(), inputformat, table)
    return

