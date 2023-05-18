import os
import glob
import importlib
import importlib.util
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

async def hello_world():
    return {"message": "Hello World!"}

app.add_api_route("/api", hello_world, methods=["GET"])

# Add all +server.py routes to web_app
for module_path in glob.glob('./**/+server.py', recursive=True):

    module_name_joined = module_path[2:].replace(os.path.sep, '.')
    module_name, module_package = module_name_joined.rsplit('.', maxsplit=1)
    
    api_route = module_path[1:] if module_path.startswith('./') else module_path
    api_route = str(Path(api_route).parent)

    mod = importlib.import_module(module_name, module_package)

    if hasattr(mod, 'GET'):
        app.add_api_route(api_route, mod.GET, methods=["GET"])
        print(f"PYTHON ENDPOINT: Added {module_path} [GET] at {api_route}")

    if hasattr(mod, 'POST'):
        app.add_api_route(api_route, mod.POST, methods=["POST"])
        print(f"PYTHON ENDPOINT: Added {module_path} [POST] at {api_route}")

    if hasattr(mod, 'PATCH'):
        app.add_api_route(api_route, mod.PATCH, methods=["PATCH"])
        print(f"PYTHON ENDPOINT: Added {module_path} [PATCH] at {api_route}")

    if hasattr(mod, 'PUT'):
        app.add_api_route(api_route, mod.PUT, methods=["PUT"])
        print(f"PYTHON ENDPOINT: Added {module_path} [PUT] at {api_route}")

    if hasattr(mod, 'DELETE'):
        app.add_api_route(api_route, mod.DELETE, methods=["DELETE"])
        print(f"PYTHON ENDPOINT: Added {module_path} [DELETE] at {api_route}")


@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"{exc}"},
    )
