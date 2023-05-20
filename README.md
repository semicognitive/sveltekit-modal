<p align="middle">
<img width="100" alt="image" src="https://user-images.githubusercontent.com/20548516/218344678-d41f4c4a-6b1b-48cc-8553-2b9fbe2169d6.png"/>
<img width="100" alt="image" src="https://camo.githubusercontent.com/f1ac9955f30176e6183aeeeac1b77354c7a132696fdc77c06ef0f0bec30f258c/68747470733a2f2f6861636b616461792e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031392f30392f707974686f6e2d6c6f676f2e706e67"/>
<img width="100" alt="image" src="https://camo.githubusercontent.com/add2c9721e333f0043ac938f3dadbc26a282776e01b95b308fcaba5afaf74ae3/68747470733a2f2f6173736574732e76657263656c2e636f6d2f696d6167652f75706c6f61642f76313538383830353835382f7265706f7369746f726965732f76657263656c2f6c6f676f2e706e67"/>
</p>

# sveltekit-python-vercel

Write Python endpoints in [SvelteKit](https://kit.svelte.dev/) and seamlessly deploy them to Vercel.

- [Current Features](#current-features)
- [Installing](#installing)
- [Testing Locally](#testing-locally)
- [Deploying to Vercel](#deploying-to-vercel)
- [Example](#example)
  - [Backend Caveats](#backend-caveats)
- [Fork of `sveltekit-modal`](#fork-of-sveltekit-modal)
- [Possible future plans](#possible-future-plans)

**This is very much in beta.**

## Current Features

- Write `+server.py` files nearly the same way you would write `+server.js` files
- Deploy (quasi) automatically to Vercel Serverless

## Installing

- Open or set up your SvelteKit project
- Install SvelteKit's Vercel adapter: `pnpm i -D @sveltejs/adapter-vercel`
- Install with `pnpm i -D sveltekit-python-vercel`
- Update your `vite.config.js`

  ```javascript
  import { defineConfig } from "vite";
  import { sveltekit } from "@sveltejs/kit/vite";
  import { sveltekit_python_vercel } from "sveltekit-python-vercel/vite";

  export default defineConfig(({ command, mode }) => {
    return {
      plugins: [sveltekit_python_vercel(), sveltekit()],
    };
  });
  ```

- Update your `svelte.config.js`:

  ```javascript
  import adapter from "@sveltejs/adapter-vercel"; // Use the vercel adapter
  import { vitePreprocess } from "@sveltejs/kit/vite";

  /** @type {import('@sveltejs/kit').Config} */
  const config = {
    preprocess: vitePreprocess(),
    kit: {
      adapter: adapter(),
      moduleExtensions: [".js", ".ts", ".py"], // add ".py" to resolve +server.py endpoints
    },
  };

  export default config;
  ```

- Update your `vercel.json`

  - The build command prepares all your endpoints and copies them to the `/api` directory where Vercel looks for functions
  - Functions and Routes tell Vercel how to run and redirect function calls

  ```json
  {
    "buildCommand": "node ./node_modules/sveltekit-python-vercel/esm/src/vite/sveltekit_python_vercel/bin.mjs; vite build",
    "functions": {
      "api/**/*.py": {
        "runtime": "@vercel/python@3.0.7"
      }
    },
    "routes": [
      {
        "src": "/api/(.*)",
        "dest": "api/index.py"
      }
    ]
  }
  ```

- Write some `+server.py` endpoints. See the example section below.

## Testing Locally

Using [Poetry](https://python-poetry.org/) to manage your virtual environments with this package is recommended.

- Run `poetry init` to create a new virtual environment, and follow the steps. Or simply create a `pyproject.toml` like the one below.

  ```toml
  [tool.poetry]
  name = "sveltekit-python-example"
  version = "0.1.0"
  description = ""
  authors = ["Your Name <email@gmail.com>"]
  readme = "README.md"

  [tool.poetry.dependencies]
  python = "^3.9"
  fastapi = "^0.95.1"
  uvicorn = "^0.22.0"


  [build-system]
  requires = ["poetry-core"]
  build-backend = "poetry.core.masonry.api"
  ```

- Required packages are python3.9 (that is what Vercel's runtime uses), `fastapi`, and `uvicorn`.
- Install whatever other dependencies you need from pypi using `poetry add package-name`

- Enter your virtual env with `poetry shell`
- Run `pnpm dev` or `npm dev`
  - You should see both the usual SvelteKit server start as well as the unvicorn server (by default on `http://0.0.0.0:8000`) in the console.

## Deploying to Vercel

- At the moment this requires a tiny bit of extra labor besides just pushing to your repository. I believe this is because of the way Vercel looks for serverless functions, but I hope to make this a bit easier in the future.

- When you make changes to your python endpoints, you have to manually regenerate the `/api` folder by running:
  1. `poetry export -f requirements.txt --output requirements.txt --without-hashes`
  2. `node ./node_modules/sveltekit-python-vercel/esm/src/vite/sveltekit_python_vercel/bin.mjs`
- Then commit `requirements.txt` and the changes in `/api` and push.

Note:

- To make this a bit smoother, you can add a script to you `package.json`:
  ```json
  "scripts": {
    ...
    "py-update": "poetry export -f requirements.txt --output requirements.txt --without-hashes; node ./node_modules/sveltekit-python-vercel/esm/src/vite/sveltekit_python_vercel/bin.mjs"
  }
  ```
  - and then just run `pnpm py-update`

## Example

- Frontend: `/src/routes/py/+page.svelte`

  ```html
  <script lang="ts">
    let a = 0;
    let b = 0;
    let total = 0;

    async function pyAddPost() {
      const response = await fetch("/py", {
        method: "POST",
        body: JSON.stringify({ a, b }),
        headers: {
          "content-type": "application/json",
        },
      });
      let res = await response.json();
      total = res.sum;
    }

    async function pyAddGet() {
      const response = await fetch(`/py?a=${a}&b=${b}`, {
        method: "GET",
        headers: {
          "content-type": "application/json",
        },
      });

      let res = await response.json();
      total = res.sum;
    }
  </script>

  <h1>This is a SvelteKit page with a python backend.</h1>

  <h3>POST Example</h3>
  <form>
    <input type="number" name="a" placeholder="Number 1" bind:value="{a}" />
    <input type="number" name="b" placeholder="Number 2" bind:value="{b}" />
    <button on:click|preventDefault="{pyAddPost}">Add</button>
  </form>
  <h4>Total: {total}</h4>

  <br />

  <h3>GET Example</h3>
  <form>
    <input type="number" name="a" placeholder="Number 1" bind:value="{a}" />
    <input type="number" name="b" placeholder="Number 2" bind:value="{b}" />
    <button on:click|preventDefault="{pyAddGet}">Add</button>
  </form>
  <h4>Total: {total}</h4>
  ```

- Backend: `/src/routes/py/+server.py`

  ```python
  from pydantic import BaseModel


  class NumberSet(BaseModel):
      a: float
      b: float


  async def POST(numberSet: NumberSet):
      return {"sum": float(numberSet.a) + float(numberSet.b)}


  async def GET(a, b):
      return {"sum": float(a) + float(b)}

  ```

### Backend Caveats

There are currently a few things that have to be worked around.

- `GET` endpoints are directly fed the parameters from the url, so when you define an endpoint
- All other endpoints are fed the body as a JSON. The recommended way to deal with this is to use a pydantic model and pass it as the singular input to the function.

See the example above.

## Fork of `sveltekit-modal`

Check out the awesome [sveltekit-modal](https://github.com/semicognitive/sveltekit-modal) package by [@semicognitive](https://github.com/semicognitive), the original way to get your python code running in SvelteKit. Modal even has GPU support for running an entire ML stack within SvelteKit.

## Possible future plans

- [ ] Generate endpoints (/api folder) automatically during build
  - [ ] Auto create requirements.txt from pyproject.toml (both related to vercel functions being checked/handled before build)
- [ ] Add form actions
- [ ] Add load functions
- [ ] Add helper functions to automatically call API endpoints in project
