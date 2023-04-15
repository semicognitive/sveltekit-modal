import sys

from synchronicity import Interface
from modal.cli.import_refs import import_stub
from modal._live_reload import run_serve_loop

from .sveltekit_modal_config import config

from watchfiles import DefaultFilter

DefaultFilter.ignore_dirs = (
    '__pycache__',
    '.git',
    '.hg',
    '.svn',
    '.tox',
    '.venv',
    'site-packages',
    '.idea',
    # 'node_modules',
    '.mypy_cache',
    '.pytest_cache',
    '.hypothesis',
)


class Logger(object):
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr_name):
        return getattr(self.stream, attr_name)

    def write(self, data):
        if config.get('log'):
            sys.stderr.write(str(data))
            sys.stderr.flush()

        self.stream.write(str(data))
        self.stream.flush()

    def flush(self):
        self.stream.flush()


if __name__ == '__main__':
    run_serve_loop('sveltekit_modal.app', stdout=Logger(sys.stdout), show_progress=True)
