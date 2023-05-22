import argparse
import glob
import importlib
import importlib.util
import shutil
from pathlib import Path

import uvicorn
from fastapi import FastAPI

parser = argparse.ArgumentParser(description="Run Sveltekit Python Server")
parser.add_argument("--host", default="0.0.0.0", help="Server hostname")
parser.add_argument("--port", type=int, default=8000, help="Server port")
parser.add_argument("--root", default=".", help="Directory where the API is located")
args = parser.parse_args()

app = FastAPI()

root_dir = Path(args.root).absolute()

api_dir = Path("./sveltekit_python_vercel").absolute()

route_dir = root_dir.joinpath("src/routes")

watch_modules = [] # list of modules to watch for changes

for module_path in glob.glob(route_dir.joinpath("**/+server.py").as_posix(), recursive=True):

    abs_module_path = Path(module_path).absolute()

    watch_modules.append(abs_module_path.parent.as_posix())

    api_route = api_dir.joinpath(abs_module_path.relative_to(root_dir/ "src/routes"))

    if not api_route.parent.exists():
        api_route.parent.mkdir(parents=True)

    # copy module path to api_route
    shutil.copy(module_path, api_route.parent)

    module_name = api_route.stem

    spec = importlib.util.spec_from_file_location(module_name, api_route)

    mod = importlib.util.module_from_spec(spec)

    spec.loader.exec_module(mod)

    # Get the relative path of the module from the API directory
    rel_path = api_route.relative_to(api_dir)

    # Convert the relative path to a string and remove the file extension
    api_path = f"/{rel_path.parent}"

    if hasattr(mod, 'GET'):
        app.add_api_route(api_path, mod.GET, methods=["GET"])

    if hasattr(mod, 'get'):
        app.add_api_route(api_path, mod.get, methods=["GET"])

    if hasattr(mod, 'POST'):
        app.add_api_route(api_path, mod.POST, methods=["POST"])

    if hasattr(mod, 'post'):
        app.add_api_route(api_path, mod.post, methods=["POST"])

    if hasattr(mod, 'PATCH'):
        app.add_api_route(api_path, mod.PATCH, methods=["PATCH"])

    if hasattr(mod, 'patch'):
        app.add_api_route(api_path, mod.patch, methods=["PATCH"])

    if hasattr(mod, 'PUT'):
        app.add_api_route(api_path, mod.PUT, methods=["PUT"])

    if hasattr(mod, 'put'):
        app.add_api_route(api_path, mod.put, methods=["PUT"])

    if hasattr(mod, 'DELETE'):
        app.add_api_route(api_path, mod.DELETE, methods=["DELETE"])

    if hasattr(mod, 'delete'):
        app.add_api_route(api_path, mod.delete, methods=["DELETE"])

if __name__ == "__main__":
    uvicorn.run(
        "sveltekit_python_vercel.serve:app",
        host=args.host, 
        port=args.port,
        log_level="info",
        reload=True,
        reload_includes=[*set(watch_modules)],
        reload_excludes=[api_dir.as_posix()]
    )
