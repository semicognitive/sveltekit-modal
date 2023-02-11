import os
import re
import glob
import importlib
import importlib.util

from fastapi import FastAPI

import modal

from sveltekit_modal.sveltekit_modal_config import config

#spec = importlib.util.spec_from_file_location(name="sveltekit_modal",  location="sveltekit_modal.config.py")
#config_module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(config_module)
#config: Config = config_module.config

web_app = FastAPI()
stub = modal.Stub('sveltekit')

# Add all +server.py routes to web_app
for module_path in glob.glob('./sveltekit_modal/src/routes/**/*.py', recursive=True):
    module_route_match = re.match(r'./sveltekit_modal/src/routes(.*)/\+server.py', module_path)
    module_route = module_route_match.group(1) if module_route_match is not None else None
    if module_route is None:
        continue

    module_name_joined = module_path[2:].replace(os.path.sep, '.')
    module_name, module_package = module_name_joined.rsplit('.', maxsplit=1)

    mod = importlib.import_module(module_name, module_package)

    web_app.add_api_route(module_route, importlib.import_module(module_name, module_package).POST, methods=["POST"])


@stub.asgi(**config.get('stub_asgi'))
def app():
    return web_app
