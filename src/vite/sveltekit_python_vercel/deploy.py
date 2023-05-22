import glob
import importlib
import importlib.util
import os
from pathlib import Path, PurePosixPath

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
    
    # Replace square brackets with curly brackets
    api_route = api_route.replace('[', '{').replace(']', '}')
    
    # remove any groups from the URL
    api_route = str(PurePosixPath(*[part for part in PurePosixPath(api_route).parts if not part.startswith("(") and not part.endswith(")")]))

    mod = importlib.import_module(module_name, module_package)
    
    # Add endpoints
    for method in ["GET", "POST", "PATCH", "PUT", "DELETE"]:
        
        # Check for duplicate methods
        if hasattr(mod, method) and hasattr(mod, method.lower()):
            raise Exception(
                f"Duplicate method {method} and {method.lower()} in {api_route}"
            )
            
        elif hasattr(mod, method):
            app.add_api_route(api_route, getattr(mod, method), methods=[method])
            print(f"PYTHON ENDPOINT: Added {module_path} [{method}] at {api_route}")
        elif hasattr(mod, method.lower()):
            app.add_api_route(api_route, getattr(mod, method.lower()), methods=[method])
            print(f"PYTHON ENDPOINT: Added {module_path} [{method}] at {api_route}")

@app.exception_handler(Exception)
async def unicorn_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": f"{exc}"},
    )
