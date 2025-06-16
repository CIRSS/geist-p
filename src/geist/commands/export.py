import click
from geist.commands.cli import cli
from geist.api.export import geist_export
from geist.tools.utils import validate_dataset

@cli.group()
def export():
    """Export a dataset"""
    pass

@export.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of an RDF dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store these exported triples (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store these exported triples (default: None)')
@click.option('--outputformat', '-oformat', default='nt', type=click.Choice(['json-ld', 'n3', 'nquads', 'nt', 'hext', 'pretty-xml', 'trig', 'trix', 'turtle', 'longturtle', 'xml']), help='Format of the exported triples (default nt)')
def rdflib(dataset, outputroot, outputfile, outputformat):
    """Export an RDF dataset"""
    geist_export(datastore='rdflib', dataset=dataset, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile, 'outputformat': outputformat})

@export.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of a SQL dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the exported table (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the exported table (default: None)')
@click.option('--outputformat', '-oformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the exported table (default csv)')
@click.option('--table', '-t', default='df', type=str, help='Name of the table to be exported (default "df")')
def duckdb(dataset, outputroot, outputfile, outputformat, table):
    """Export a SQL dataset"""
    (_, conn) = geist_export(datastore='duckdb', dataset=dataset, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile, 'outputformat': outputformat, 'table': table})
    conn.close()

@export.command()
@click.option('--dataset', '-d', default='kb', type=str, callback=validate_dataset, help='Name of an ASP dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the exported data (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the exported data (default: None). This file can be reused to create a dataset by setting inputformat=json.')
@click.option('--returnformat', '-rformat', default='lp', type=click.Choice(['lp', 'df', 'dict']), help='Format of the returned data in memory (default lp)')
@click.option('--predicate', '-pred', default=None, type=str, help='Name of the predicate to be exported (default "predicate")')
def clingo(dataset, outputroot, outputfile, returnformat, predicate):
    """Export an ASP dataset"""
    geist_export(datastore='clingo', dataset=dataset, hasoutput=True, config={'outputroot': outputroot, 'outputfile': outputfile, 'returnformat': returnformat, 'predicate': predicate})
