import sys
import traceback

from synchronicity import Interface
from modal.cli.app import _show_stub_ref_failure_help
from modal_utils.async_utils import synchronizer
from modal_utils.package_utils import NoSuchStub, import_stub, parse_stub_ref

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
    #'node_modules',
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
    parsed_stub_ref = parse_stub_ref('sveltekit_modal.app')
    try:
        stub = import_stub(parsed_stub_ref)
    except NoSuchStub:
        _show_stub_ref_failure_help(parsed_stub_ref)
        sys.exit(1)
    except Exception:
        traceback.print_exc()
        sys.exit(1)

    _stub = synchronizer._translate_in(stub)
    blocking_stub = synchronizer._translate_out(_stub, Interface.BLOCKING)
    blocking_stub.serve(stdout=Logger(sys.stdout), show_progress=True)
