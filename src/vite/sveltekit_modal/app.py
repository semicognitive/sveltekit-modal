import os
import re
import glob
import importlib
import importlib.util

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import modal

from .sveltekit_modal_config import config

#spec = importlib.util.spec_from_file_location(name="sveltekit_modal",  location="sveltekit_modal.config.py")
#config_module = importlib.util.module_from_spec(spec)
# spec.loader.exec_module(config_module)
#config: Config = config_module.config

web_app = FastAPI()
stub = modal.Stub(config.get('name'))

# Add all +server.py routes to web_app
for module_path in glob.glob('./sveltekit_modal/src/routes/**/*.py', recursive=True):
    module_route_match = re.match(r'./sveltekit_modal/src/routes(.*)/\+server.py', module_path)
    module_route = module_route_match.group(1) if module_route_match is not None else None
    if module_route is None:
        continue

    module_name_joined = module_path[2:].replace(os.path.sep, '.')
    module_name, module_package = module_name_joined.rsplit('.', maxsplit=1)

    mod = importlib.import_module(module_name, module_package)

    if hasattr(mod, 'GET'):
        web_app.add_api_route(module_route, mod.GET, methods=["GET"])

    if hasattr(mod, 'POST'):
        web_app.add_api_route(module_route, mod.POST, methods=["POST"])

    if hasattr(mod, 'PATCH'):
        web_app.add_api_route(module_route, mod.PATCH, methods=["PATCH"])

    if hasattr(mod, 'PUT'):
        web_app.add_api_route(module_route, mod.PUT, methods=["PUT"])

    if hasattr(mod, 'DELETE'):
        web_app.add_api_route(module_route, mod.DELETE, methods=["DELETE"])


@web_app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"{exc}"},
    )


@stub.function(**config.get('stub_asgi'))
@stub.asgi_app()
def app():
    return web_app
