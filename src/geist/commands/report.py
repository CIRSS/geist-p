import click, json, sys
from geist.commands.cli import cli
from geist.api.report import geist_report

@cli.command()
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the report template to expand')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the expanded report (default: current directory)')
@click.option('--suppressoutput', '-so', default=False, help='Suppress output or not (default: False)')
def report(inputfile, outputroot, suppressoutput):
    """Expand a report using dataset(s)"""
    geist_report(inputfile=inputfile.read(), isinputpath=False, outputroot=outputroot, suppressoutput=suppressoutput)
