import click

@click.group()
def cli():
    global outputroot
    outputroot = './'
    pass