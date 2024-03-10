import click, sys
from geist.commands.cli import cli

@cli.group()
def create():
    """Create a new dataset"""
    pass

@create.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
@click.option('--infer', default='none', type=click.Choice(['none', 'rdfs', 'owl', 'rdfs_owl']), help='Inference to perform on update [none, rdfs, owl, rdfs_owl] (default "none")')
def rdflib(dataset, inputfile, inputformat, colnames, infer):
    """Create a new RDF dataset using RDFLib"""
    from geist.datastore.rdflib import rdflib_create
    rdflib_create(dataset, inputfile.read(), inputformat, colnames, infer)

@create.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of SQL dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as a Pandas DataFrame')
@click.option('--inputformat', '-iformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the file to be loaded as a Pandas DataFrame (default csv)')
@click.option('--table', '-t', default='df', type=str, help='Name of the table to be created (default "df")')
def duckdb(dataset, inputfile, inputformat, table):
    """Create a new SQL dataset using DuckDB"""
    from geist.datastore.duckdb import duckdb_create
    duckdb_create(dataset, inputfile.read(), inputformat, table)
    pass


