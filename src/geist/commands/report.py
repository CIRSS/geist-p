import click, json, sys, ast
from geist.commands.cli import cli
from geist.api.report import geist_report

@cli.command()
@click.option('--inputfile', '-ifile', required=True, type=click.File('r'), default=sys.stdin, help='Path of the file containing the report template to expand')
@click.option('--outputroot', '-oroot', default='./', type=str, help='Path of the directory to store the expanded report (default: current directory)')
@click.option('--suppressoutput', '-so', default=False, help='Suppress output or not (default: False)')
@click.option('--args', '-a', type=(str, str), default=None, multiple=True, help='Arguments to be passed to the report template, e.g., (arg, value) indicates that {{ arg }} in the report template will be replaced by value')
def report(inputfile, outputroot, suppressoutput, args):
    """Expand a report using dataset(s)"""
    formatted_args = {}
    for arg in args:
        formatted_args[arg[0]] = arg[1]
    geist_report(inputfile=inputfile.read(), isinputpath=False, outputroot=outputroot, suppressoutput=suppressoutput, args=formatted_args)
