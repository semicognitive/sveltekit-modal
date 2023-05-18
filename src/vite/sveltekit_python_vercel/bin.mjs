#!/usr/bin/env zx --install

import {$} from "zx";

const python_path = await $`which python3`;
await $`${python_path} ./node_modules/sveltekit-python-vercel/esm/src/vite/sveltekit_python_vercel/build.py --root . --packagedir ./node_modules/sveltekit-python-vercel/esm/src/vite/sveltekit_python_vercel`;
