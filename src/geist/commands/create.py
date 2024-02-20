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
    """Create a new RDF dataset"""
    from geist.datastore.rdflib import rdflib_create
    rdflib_create(dataset, inputfile.read(), inputformat, colnames, infer)

@create.command()
def duckdb():
    """Create a new SQL dataset using DuckDB"""
    print("Creating a new SQL dataset using DuckDB")
    pass


