<img width="100" alt="image" src="https://user-images.githubusercontent.com/20548516/218344678-d41f4c4a-6b1b-48cc-8553-2b9fbe2169d6.png"/>
<img width="100" alt="image" src="https://camo.githubusercontent.com/f1ac9955f30176e6183aeeeac1b77354c7a132696fdc77c06ef0f0bec30f258c/68747470733a2f2f6861636b616461792e636f6d2f77702d636f6e74656e742f75706c6f6164732f323031392f30392f707974686f6e2d6c6f676f2e706e67"/>
<img width="100" alt="image" src="https://camo.githubusercontent.com/add2c9721e333f0043ac938f3dadbc26a282776e01b95b308fcaba5afaf74ae3/68747470733a2f2f6173736574732e76657263656c2e636f6d2f696d6167652f75706c6f61642f76313538383830353835382f7265706f7369746f726965732f76657263656c2f6c6f676f2e706e67"/>

# sveltekit-python-vercel

Write Python endpoints in [SvelteKit](https://kit.svelte.dev/) and seamlessly deploy them to Vercel.

**This is very much in beta.**

## Current Features

- Write `+server.py` files nearly the same way you would write `+server.js` files
- These functions deploy automatically to Vercel Serverless

## Installing

- Open or set up your SvelteKit project
- Install with `npm i -D sveltekit-python-vercel`
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
  import adapter from "@sveltejs/adapter-vercel";
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



## Caveats

There are currently a few things that have to be worked around.

## Fork of `sveltekit-modal`

Check out the awesome [sveltekit-modal](https://github.com/semicognitive/sveltekit-modal) package by [@semicognitive](https://github.com/semicognitive), the original way to get your python code running in SvelteKit. Modal even has GPU support for running an entire ML stack within SvelteKit.

## Possible future plans

- [ ] Generate endpoints (/api folder) automatically during build
  - [ ] Auto create requirements.txt from pyproject.toml (both related to vercel functions being checked/handled before build)
- [ ] Add form actions
- [ ] Add load functions
- [ ] Add helper functions to automatically call API endpoints in project
