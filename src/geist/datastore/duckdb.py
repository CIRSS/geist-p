import click

@click.group()
def cli():
    pass

@cli.group()
def sql_duckdb():
    pass

@sql_duckdb.command()
def create():
    click.echo("Creating tables")

@sql_duckdb.command()
def load():
    click.echo("Loading tables")

if __name__ == '__main__':
    cli()
