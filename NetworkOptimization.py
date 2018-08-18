import click
from tests import NetworkTest as tests

@click.group()
@click.pass_context
def cli(context):
    pass

cli.add_command(tests.init)

if __name__=='__main__':
    cli()