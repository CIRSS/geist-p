import click, sys
from geist.commands.cli import cli
from geist.api.query import geist_query
from geist.tools.utils import validate_dataset

@cli.group()
def query():
    """Perform a query on a dataset"""
    pass

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of RDF dataset to be queried (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Specify either the path of the file containing the SPARQL query to execute or provide the SPARQL query itself via stdin')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def rdflib(dataset, inputfile, outputroot, outputfile):
    """Perform a SPARQL query on a dataset"""
    geist_query(datastore='rdflib', dataset=dataset, inputfile=inputfile.read(), isinputpath=False, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile})

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of SQL dataset to be queried (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Specify either the path of the file containing the SQL query to execute or provide the SQL query itself via stdin')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def duckdb(dataset, inputfile, outputroot, outputfile):
    """Perform a SQL query on a dataset"""
    (_, conn) = geist_query(datastore='duckdb', dataset=dataset, inputfile=inputfile.read(), isinputpath=False, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile})
    conn.close()

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of ASP dataset to be queried (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Specify either the path of the file containing the ASP query to execute or provide the ASP query itself via stdin')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
@click.option('--outputformat', '-oformat', default='lp', type=click.Choice(['lp', 'csv']), help='Format of the exported data (default lp)')
@click.option('--predicate', '-pred', default=None, type=str, help='Name of the predicate to be queried')
@click.option('--programname', '-prog', default='base', type=str, help='Name of the program')
def clingo(dataset, inputfile, outputroot, outputfile, outputformat, predicate, programname):
    """Perform an ASP query on a dataset"""
    geist_query(datastore='clingo', dataset=dataset, inputfile=inputfile.read(), isinputpath=False, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile, 'outputformat': outputformat, 'predicate': predicate, 'programname': programname})