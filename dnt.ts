import { build } from "dnt";
import { copy, emptyDir } from "fs";

import denoconfig from "./deno.json" assert { type: "json" };

await emptyDir("./npm");

await build({
  entryPoints: ["./mod.ts", {
    name: "./vite",
    path: "./src/vite/mod.ts",
  }],
  outDir: "./npm",
  typeCheck: true,
  declaration: true,
  scriptModule: false,
  test: false,
  importMap: denoconfig.importMap,
  compilerOptions: {
    lib: ["es2021", "dom", "dom.iterable"],
  },
  shims: {},
  package: {
    name: denoconfig.package.name,
    version: Deno.args[0],
    description: denoconfig.package.description,
    repository: {
      type: "git",
      url: `git+https://github.com/${denoconfig.package.github}.git`,
    },
    homepage: `https://github.com/${denoconfig.package.github}#readme`,
    license: "MIT",
    bin: "./bin.mjs",
    exports: {
      ".": {
        "import": "./esm/mod.js",
        "types": "./types/mod.d.ts",
      },
      "./vite": {
        "import": "./esm/src/vite/mod.js",
        "types": "./types/src/vite/mod.d.ts",
      },
      "./package.json": "./package.json",
    },
    //Legacy manual stuff for moduleResolution: node
    "types": "./types/mod.d.ts",
    "typesVersions": {
      "*": {
        "vite": [
          "./types/src/vite/mod.d.ts",
        ],
      },
    },
    keywords: [
      denoconfig.package.name,
      "svelte-kit",
      "sveltekit",
      "svelte",
      "modal",
      "python",
    ],
    engines: {
      "node": ">=16.0.0",
    },
    author: denoconfig.package.github.split("/")[0],
    bugs: {
      url: `https://github.com/${denoconfig.package.github}/issues`,
    },
    dependencies: {
      "zx": "^7.0.0",
      "rollup-plugin-globsync": "ConProgramming/rollup-plugin-globsync#650e6b4", //update ref
    },
    peerDependencies: {
      "vite": "^4.0.0",
    },
  },
});

// post build steps
await copy("LICENSE.md", "npm/LICENSE.md");
await copy("README.md", "npm/README.md");
await copy("src/bin.mjs", "npm/bin.mjs");
await copy("src/vite/sveltekit_modal", "npm/esm/src/vite/sveltekit_modal");
