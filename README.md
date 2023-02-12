<img width="800" alt="image" src="https://user-images.githubusercontent.com/20548516/215316618-bcb365fa-d4d7-49d8-8832-21ed849e2060.png">

# sveltekit-modal

Write Python endpoints in [SvelteKit](https://kit.svelte.dev/) using [Modal](https://modal.com)

Made with [this template](https://github.com/semicognitive/es-package/generate)

## Why
- Start deploying **Python endpoints** in **just a few steps**.
- GPU support for an entire ML Stack in your SvelteKit app
- 

## Add to your SvelteKit project
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
  - Write your endpoints! See an example [here]().
