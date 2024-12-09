import click
from geist.commands.cli import cli
from geist.api.destroy import geist_destroy

@cli.group()
def destroy():
    """Delete a dataset"""
    pass

@destroy.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of RDF dataset to be removed (default "kb")')
@click.option('--quiet', '-q', is_flag=True, show_default=True, default=False, help="Suppress error messages if the provided dataset does not exist")
def rdflib(dataset, quiet):
    """Delete an RDF dataset"""
    geist_destroy(datastore='rdflib', dataset=dataset, quiet=quiet)

@destroy.command()
@click.option('--dataset', '-d', default='kb', type=str, help='Name of SQL dataset to be removed (default "kb")')
@click.option('--quiet', '-q', is_flag=True, show_default=True, default=False, help="Suppress error messages if the provided dataset does not exist")
def duckdb(dataset, quiet):
    """Delete a SQL dataset"""
    geist_destroy(datastore='duckdb', dataset=dataset, quiet=quiet)
