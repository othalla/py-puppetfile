import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from cliff.lister import Lister

ENVS = ['dev', 'production']


class MyApp(App):
    def __init__(self):
        super().__init__(
            description='Command line for puppet control repository',
            version='0.1',
            command_manager=CommandManager('myapp'),
            deferred_help=True,
        )

    def initialize_app(self, argv):
        commands = [Environment]
        for command in commands:
            self.command_manager.add_command(command.__name__.lower(), command)


class Environment(Lister):
    """List all Puppet environments"""

    def get_parser(self, prog_name):
        parser = super().get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        return (('Name',), ((env,) for env in ENVS))


def main():
    argv = sys.argv[1:]
    myapp = MyApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main())
