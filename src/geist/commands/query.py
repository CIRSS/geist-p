import click, sys
from geist.commands.cli import cli
from geist.api.query import geist_query

@cli.group()
def query():
    """Perform a query on a dataset"""
    pass

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be queried (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Specify either the path of the file containing the SPARQL query to execute or provide the SPARQL query itself via stdin')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def rdflib(dataset, inputfile, outputroot, outputfile):
    """Perform a SPARQL query on a dataset"""
    geist_query(datastore='rdflib', dataset=dataset, inputfile=inputfile.read(), isinputpath=False, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile})

@query.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be queried (default "kb")')
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Specify either the path of the file containing the SQL query to execute or provide the SQL query itself via stdin')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the query results (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the query results (default: None)')
def duckdb(dataset, inputfile, outputroot, outputfile):
    """Perform a SQL query on a dataset"""
    geist_query(datastore='duckdb', dataset=dataset, inputfile=inputfile.read(), isinputpath=False, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile})
