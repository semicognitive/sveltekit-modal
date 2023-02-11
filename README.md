<img width="800" alt="image" src="https://user-images.githubusercontent.com/20548516/215316618-bcb365fa-d4d7-49d8-8832-21ed849e2060.png">

# es-package

The ultimate template for creating and publishing an ES module

Start by [using this template](https://github.com/semicognitive/es-package/generate)

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
