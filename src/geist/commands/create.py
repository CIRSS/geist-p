import click, sys
from geist.commands.cli import cli
from geist.api.create import geist_create
from geist.tools.utils import validate_dataset

@cli.group()
def create():
    """Create a new dataset"""
    pass

@create.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of RDF dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as triples')
@click.option('--inputformat', '-iformat', default='json-ld', type=click.Choice(['xml', 'n3', 'turtle', 'nt', 'pretty-xml', 'trix', 'trig', 'nquads', 'json-ld', 'hext', 'csv']), help='Format of the file to be loaded as triples (default json-ld)')
@click.option('--colnames', default=None, type=str, help='Column names of triples with the format of [[subject1, predicate1, object1], [subject2, predicate2, object2], ...] when the input format is csv')
@click.option('--infer', default='none', type=click.Choice(['none', 'rdfs', 'owl', 'rdfs_owl']), help='Inference to perform on update [none, rdfs, owl, rdfs_owl] (default "none")')
def rdflib(dataset, inputfile, inputformat, colnames, infer):
    """Create a new RDF dataset using RDFLib"""
    geist_create(datastore='rdflib', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'colnames': colnames, 'infer': infer})

@create.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of SQL dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as a Pandas DataFrame')
@click.option('--inputformat', '-iformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the file to be loaded as a Pandas DataFrame (default csv)')
@click.option('--table', '-t', default='df', type=str, help='Name of the table to be created (default "df")')
def duckdb(dataset, inputfile, inputformat, table):
    """Create a new SQL dataset using DuckDB"""
    conn = geist_create(datastore='duckdb', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'table': table})
    conn.close()

@create.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of ASP dataset to create (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file to be loaded as facts, rules, and contraints')
@click.option('--inputformat', '-iformat', default='lp', type=click.Choice(['lp', 'csv']), help='Format of the file to be loaded as facts, rules, and constraints. Note that "csv" only supports facts (default "lp")')
@click.option('--predicate', '-pred', default='isfirstcol', type=str, help='"isfirstcol" for using the first column as the predicate name; strings other than "isfirstcol" are used as the predicate name directly (default: "isfirstcol")')
@click.option('--programname', '-prog', default='base', type=str, help='Name of the program (default: "base")')
def clingo(dataset, inputfile, inputformat, predicate, programname):
    """Create a new ASP dataset using Clingo"""
    geist_create(datastore='clingo', dataset=dataset, inputfile=inputfile.read(), inputformat=inputformat, isinputpath=False, config={'predicate': predicate, 'programname': programname})
