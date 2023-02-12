<img width="800" alt="image" src="https://user-images.githubusercontent.com/20548516/215316618-bcb365fa-d4d7-49d8-8832-21ed849e2060.png">

# sveltekit-modal

Write Python endpoints in [SvelteKit](https://kit.svelte.dev/) using [Modal](https://modal.com)

Made with [this template](https://github.com/semicognitive/es-package/generate)

## Add to your SvelteKit project
Start deploying Python endpoints, with GPU support for an entire ML Stack in your app, in just a few steps.r

- Install `npm i -D sveltekit-modal`
- Sign up for [modal.com](https://modal.com/signup), the serverless python platform. All users get $30 free monthly credits!
- Update `vite.config.js`
```javascript
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

import { sveltekit_modal } from 'sveltekit-modal/vite'; //Add this import

export default defineConfig({
	plugins: [sveltekit_modal(), sveltekit()] //Add the `sveltekit_modal()` plugin
});
```
- Update `svelte.config.js`
```javascript
import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/kit/vite';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	preprocess: vitePreprocess(),
	kit: {
		adapter: adapter(),
		moduleExtensions: [".js", ".ts", ".py"] //Add this line, to resolve +server.py endpoints
	}
};

export default config;
```
- Create `sveltekit_modal_config.py`. The option `stub_asgi` is passed to [Modal](https://modal.com/docs/reference/modal.Stub#asgi). This is where you can define GPU acceleration, secrets, and an Image for pip installs, etc. Explore their [docs](https://modal.com/docs/guide)!
```python
import modal
import sveltekit_modal

config: sveltekit_modal.Config = {
    'log': False,
    'stub_asgi': {
        'image': modal.Image.debian_slim()
    }
}
```



## Why
- Fast iterating thanks to [Deno](https://deno.land/), for built in Typescript debugging and bundling
- Easily import into [Replit](https://replit.com/), for an instant dev environment
- I'm dogfooding it - using it [myself](https://github.com/semicognitive/thefuz)
- Immediately works for Deno, Bun, Node, Cloudflare Workers, etc.
- Publish to NPM in **_seconds_**

## Publish
Easily publish to [deno.land/x](https://deno.land/x) and [npm](https://npmjs.com)

### Deno
- Follow https://deno.land/add_module
- Create a [release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release)

### Npm
- Add a [action secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) of [`NPM_ACCESS_TOKEN`](https://docs.npmjs.com/creating-and-viewing-access-tokens#creating-access-tokens)
- Create a [release](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository#creating-a-release)
