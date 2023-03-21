<img width="200" alt="image" src="https://user-images.githubusercontent.com/20548516/218344678-d41f4c4a-6b1b-48cc-8553-2b9fbe2169d6.png"/><img width="200" alt="image" src="https://user-images.githubusercontent.com/20548516/219166985-96888b52-51de-4f6b-b37d-cc66264c40eb.png"/>

# sveltekit-modal
Write Python endpoints in [SvelteKit](https://kit.svelte.dev/) using [Modal](https://modal.com).

## Why
- Start deploying **Python endpoints** in **just a few steps**
- GPU support for an entire ML Stack in your SvelteKit app
- Integrates completely, write `+server.py` just like your `+server.js` files
- Deploy the rest of your app anywhere, with [SvelteKit's adapters for Vercel, Netlify, Cloudflare, etc.](https://kit.svelte.dev/docs/adapters)
- Serverless Python with [ease](https://kit.svelte.dev/docs/adapters)

## Add to your SvelteKit project
- Open a [new](https://kit.svelte.dev/docs/creating-a-project) or **existing** SvelteKit Project
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

    config = {
        'name': 'sveltekit-example',
        'log': False,
        'stub_asgi': {
            'image': modal.Image.debian_slim()
        }
    }
    ```
  - Update `.gitignore`, add `!.env.production`.
  - Write your endpoints! See an example [here](https://github.com/semicognitive/sveltekit-modal-langchain).

## Use
- Develop like a normal SvelteKit app, just `npm run dev`
- Deploy all your python endpoints with one command, just `npx sveltekit-modal deploy`

## Examples

The `example_app/` directory contains an incredibly bare and demonstrates how to get it working.

- [semicognitive/sveltekit-modal-langchain](https://github.com/semicognitive/sveltekit-modal-langchain) demonstrates a nice version of the library with [langchain](https://github.com/hwchase17/langchain) and [tailwindcss](https://tailwindcss.com/)