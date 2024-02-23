import click
from geist.commands.cli import cli

@cli.group()
def destroy():
    """Delete a dataset"""
    pass

@destroy.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be removed (default "kb")')
@click.option('--quiet', '-q', is_flag=True, show_default=True, default=False, help="Suppress error messages if the provided dataset does not exist")
def rdflib(dataset, quiet):
    """Delete an RDF dataset"""
    from geist.datastore.rdflib import rdflib_destroy
    rdflib_destroy(dataset=dataset, quiet=quiet)

@destroy.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of SQL dataset to be removed (default "kb")')
@click.option('--quiet', '-q', is_flag=True, show_default=True, default=False, help="Suppress error messages if the provided dataset does not exist")
def duckdb(dataset, quiet):
    """Delete a SQL dataset"""
    from geist.datastore.duckdb import duckdb_destroy
    duckdb_destroy(dataset=dataset, quiet=quiet)
    return
