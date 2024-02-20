#!/usr/bin/env python3

from geist.commands.cli import cli
from geist.commands.create import create
from geist.commands.load import load
from geist.commands.destroy import destroy
from geist.commands.export import export
from geist.commands.query import query
from geist.commands.graph import graph
from geist.commands.report import report

# Add commands
cli.add_command(create)
cli.add_command(load)
cli.add_command(destroy)
cli.add_command(export)
cli.add_command(query)
cli.add_command(graph)
cli.add_command(report)

if __name__ == '__main__':
    cli()
