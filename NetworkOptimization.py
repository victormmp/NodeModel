"""
Main application script.

This file sums all working options for the entire application.

 COMMANDS:

 => test-model
    - Perform specific simulated tests on the alghorithm.
      see './tests/NetworkTest.py' for references.

"""


import click

from tests import NetworkTest as tests


@click.group()
@click.pass_context
def cli(context):
    pass

# ADD COMMANDS
cli.add_command(tests.init)

if __name__=='__main__':
    cli()
