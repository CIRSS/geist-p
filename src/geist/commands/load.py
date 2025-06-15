import click, sys
from geist.commands.cli import cli
from geist.api.load import geist_load
from geist.tools.utils import validate_dataset

@cli.group()
def load():
    """Import data into a dataset"""
    pass

@load.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of an RDF dataset to load a file (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
def rdflib(dataset, inputfile, inputformat, colnames):
    """Import data into a RDF dataset"""
    geist_load(datastore='rdflib', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'colnames': colnames, 'inmemory': False})

@load.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of a SQL dataset to load a file (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as a table')
@click.option('--inputformat', '-iformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the file to be loaded as a table (default csv)')
@click.option('--table', '-t', required=True, type=str, help='Name of the table to be created')
def duckdb(dataset, inputfile, inputformat, table):
    """Import data into a SQL dataset"""
    conn = geist_load(datastore='duckdb', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'table': table, 'inmemory': False})
    conn.close()

@load.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of an ASP dataset to load a file (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded')
@click.option('--inputformat', '-iformat', default='lp', type=click.Choice(['lp', 'csv']), help='Format of the file to be loaded (default "lp")')
@click.option('--predicate', '-pred', default='isfirstcol', type=str, help='Name of the predicate to be loaded (default: "isfirstcol")')
@click.option('--programname', '-prog', default='base', type=str, help='Name of the program (default: "base")')
def clingo(dataset, inputfile, inputformat, predicate, programname):
    """Import data into an ASP dataset"""
    geist_load(datastore='clingo', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'predicate': predicate, 'programname': programname, 'inmemory': False})
