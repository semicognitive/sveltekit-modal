import argparse
import shutil
import glob

from pathlib import Path, PurePosixPath

parser = argparse.ArgumentParser(description="Run Sveltekit Python Deployment")
parser.add_argument("--root", default=".", help="Root directory of Vercel project")
parser.add_argument("--packagedir", default=None, help="Root directory of Vercel project")
args = parser.parse_args()


root_dir = Path(args.root).absolute()
api_dir = root_dir / "api"

if not api_dir.exists():
    api_dir.mkdir()
    
if args.packagedir:
    shutil.copy(Path(args.packagedir).absolute() / "deploy.py", api_dir / "index.py")
    

# Add all +server.py routes to web_app
for module_path in glob.glob(str(root_dir / 'src/routes/**/+server.py'), recursive=True):
    
    # replace the root_dir with api_dir
    api_route = api_dir / Path(module_path).absolute().relative_to(root_dir / "src/routes")
    
    # replace square brackets with curly brackets
    api_route = Path(str(api_route).replace('[', '{').replace(']', '}'))
    
    # remove any groups from the URL
    api_route = Path(str(PurePosixPath(*[part for part in PurePosixPath(api_route).parts if not part.startswith("(") and not part.endswith(")")])))

    if not api_route.parent.exists():
        api_route.parent.mkdir(parents=True)
    
    # copy module path to api_route
    shutil.copy(module_path, api_route.parent)
    
    # create __init__.py if it doesn't exist
    if not (api_route.parent / "__init__.py").exists():
        (api_route.parent / "__init__.py").touch()
    
    print(f"PYTHON ENDPOINT: Copied {module_path} to {api_route.parent}")
