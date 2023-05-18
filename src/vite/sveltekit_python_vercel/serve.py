import uvicorn
import argparse
import os
import importlib
import importlib.util
import glob
import shutil
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

parser = argparse.ArgumentParser(description="Run Sveltekit Python Server")
parser.add_argument("--host", default="0.0.0.0", help="Server hostname")
parser.add_argument("--port", type=int, default=8000, help="Server port")
parser.add_argument("--root", default=".", help="Directory where the API is located")
args = parser.parse_args()

app = FastAPI()

def app_factory():
    return app # return the app object

if __name__ == "__main__":
    
    root_dir = Path(args.root).absolute()
    api_dir = Path("./sveltekit_python_vercel").absolute()

    # Add all +server.py routes to web_app
    for module_path in glob.glob(str(root_dir / 'src/routes/**/+server.py'), recursive=True):
        
        # replace the root_dir with api_dir
        api_route = api_dir / Path(module_path).absolute().relative_to(root_dir/ "src/routes")
        
        if not api_route.parent.exists():
            api_route.parent.mkdir(parents=True)
        
        # copy module path to api_route
        shutil.copy(module_path, api_route.parent)
        print(f"PYTHON ENDPOINT: Copied {module_path} to {api_route.parent}")
        
        # Get the module name from the module path
        module_name = api_route.stem
        
        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(module_name, api_route)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        
        # Get the relative path of the module from the API directory
        rel_path = api_route.relative_to(api_dir)
        # Convert the relative path to a string and remove the file extension
        api_path = "/" + str(rel_path.parent)
        
        print("ADDING API PATH:", rel_path, api_path)
        
        if hasattr(mod, 'GET'):
            app.add_api_route(api_path, mod.GET, methods=["GET"])

        if hasattr(mod, 'POST'):
            app.add_api_route(api_path, mod.POST, methods=["POST"])

        if hasattr(mod, 'PATCH'):
            app.add_api_route(api_path, mod.PATCH, methods=["PATCH"])

        if hasattr(mod, 'PUT'):
            app.add_api_route(api_path, mod.PUT, methods=["PUT"])

        if hasattr(mod, 'DELETE'):
            app.add_api_route(api_path, mod.DELETE, methods=["DELETE"])

    
    config = uvicorn.Config(app_factory, host=args.host, port=args.port, log_level="info", factory=True)
    server = uvicorn.Server(config)
    print(f"Hosting on http://{args.host}:{args.port}")
    server.run()
