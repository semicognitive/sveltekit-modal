import { build, emptyDir } from "dnt";

import denoconfig from "./deno.json" assert { type: "json" };

await emptyDir("./npm");

await build({
  entryPoints: ["./mod.ts"],
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
    main: "./esm/mod.js",
    types: "./types/mod.d.ts",
    exports: {
      ".": {
        "import": "./esm/mod.js",
        "require": "./script/mod.js",
      },
      "./package.json": "./package.json",
    },
    keywords: [
      denoconfig.package.name,
    ],
    engines: {
      "node": ">=16.0.0",
    },
    author: denoconfig.package.github.split('/')[0],
    bugs: {
      url: `https://github.com/${denoconfig.package.github}/issues`,
    },
  },
});

// post build steps
Deno.copyFileSync("LICENSE.md", "npm/LICENSE.md");
Deno.copyFileSync("README.md", "npm/README.md");
