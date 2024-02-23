import click
from geist.commands.cli import cli

@cli.group()
def export():
    """Export a dataset"""
    pass

@export.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store these exported triples (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store these exported triples (default: None)')
@click.option('--outputformat', '-oformat', default='nt', type=click.Choice(['json-ld', 'n3', 'nquads', 'nt', 'hext', 'pretty-xml', 'trig', 'trix', 'turtle', 'longturtle', 'xml']), help='Format of the exported triples (default nt)')
def rdflib(dataset, outputroot, outputfile, outputformat):
    """Export an RDF dataset"""
    from geist.datastore.rdflib import rdflib_export
    rdflib_export(dataset, outputroot, outputfile, outputformat)

@export.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of SQL dataset to be exported (default "kb")')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the exported table (default: current directory). If the given path (i.e., --outputfile) is None or a relative path, it will be ignored.')
@click.option('--outputfile', '-ofile', default=None, type=str, help='Path of the file to store the exported table (default: None)')
@click.option('--outputformat', '-oformat', default='csv', type=click.Choice(['csv', 'json']), help='Format of the exported table (default csv)')
@click.option('--table', '-t', default='df', type=str, help='Name of the table to be exported (default "df")')
def duckdb(dataset, outputroot, outputfile, outputformat, table):
    """Export a SQL dataset"""
    from geist.datastore.duckdb import duckdb_export
    duckdb_export(dataset, outputroot, outputfile, outputformat, table)
    return
