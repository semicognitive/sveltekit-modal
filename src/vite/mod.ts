import {loadEnv, type Plugin} from "vite";
import {
  type ProcessPromise,
  $ as run$,
  cd as cd$,
  which,
  path,
  chalk,
} from "zx";

const get_pyServerEndpointAsString = (app_url: URL, serve = false) => `
    const handle = (method) => (async ({ request, fetch, url }) => {
        const headers = new Headers()
        headers.append('content-type', request.headers.get('content-type'));
        headers.append('accept', request.headers.get('accept'));

        let fullURL;

        if (${serve}) {
          fullURL = new URL(url.pathname, new URL('${app_url}')) + url.search;
        } else {
          fullURL = new URL('/api' + url.pathname, new URL('${app_url}')) + url.search;
        }

        console.log(\`Reached python endpoint of \${method} \${fullURL}\`)
        let requestBody = await request.clone().text();
        console.log(\`Body: \${requestBody}\`);
        console.log(\`Content-Type: \${request.headers.get('content-type')}\`);

        if (method === 'GET') {
          requestBody = null;
        }

        return fetch(fullURL, { headers, method, body: requestBody, signal: request.signal, duplex: 'half' });
    });
    
    export const GET = handle('GET');
    export const POST = handle('POST');
    export const PATCH = handle('PATCH');
    export const PUT = handle('PUT');
    export const DELETE = handle('DELETE');
`;

export interface SveltekitPythonOptions {
  python_path?: string;
  log?: boolean;
  host?: string;
  port?: number;
}

export async function sveltekit_python_vercel(
  opts: SveltekitPythonOptions = {}
): Promise<Plugin[]> {
  const child_processes: ProcessPromise[] = [];
  async function kill_all_process() {
    for (const ps of child_processes) {
      await ps.kill();
      await ps.exitCode;
    }
  }

  let sveltekit_url: URL | undefined;

  const plugin_python_serve: Plugin = {
    name: "vite-plugin-sveltekit-python-serve",
    apply: "serve",
    async closeBundle() {
      await kill_all_process();
    },
    async configureServer({config}) {
      const packagelocation = path.join(
        config.root,
        "node_modules",
        "sveltekit-python-vercel",
        "esm/src/vite"
      );

      // copy asll +server.py files to package directory

      run$.verbose = false;
      run$.env.PYTHONDONTWRITEBYTECODE = "1";

      cd$(packagelocation);

      const python_path = opts.python_path ?? (await which("python3"));
      const host = opts.host ?? "0.0.0.0";
      const port = opts.port ?? 8000;
      const local_process: ProcessPromise = run$`${python_path} -m sveltekit_python_vercel.serve --host ${host} --port ${port} --root ${config.root}`;
      child_processes.push(local_process);

      sveltekit_url ??= new URL(`http://${host}:${port}`);

      cd$(config.root);

      // local_process.quiet();  // let it be loud for now
      local_process.nothrow();

      local_process.stderr.on("data", (s) => {
        console.log(s.toString().trimEnd()); //Logs stderr always and all of stdout if 'log': True
      });
      local_process.stderr.on("error", (s) => {
        console.error(chalk.red("Error: Python Serve Failed"));
        console.error(s.toString().trimEnd());
      });

      local_process.stdout.on("error", (s) => {
        console.error(chalk.red("Error: Python Serve Failed"));
        console.error(s.toString().trimEnd());
      });
    },
  };

  const plugin_python_build: Plugin = {
    name: "vite-plugin-sveltekit_python-build",
    apply: "build",
    async configResolved(config) {
      console.log("Generate requirements.txt...");

      await run$ `poetry export -f requirements.txt --output requirements.txt --without-hashes`;

      console.log("BUILD DEBUG");

      console.log("ROOT PATH: " + config.root);
      console.log(
        "LOADED VERCEL URL: " + loadEnv("", config.root, "").VERCEL_URL
      );

      const packagelocation = path.join(
        config.root,
        "node_modules",
        "sveltekit-python-vercel",
        "esm/src/vite"
      );

      console.log("PACKAGE LOCATION: " + packagelocation);

      const python_path = opts.python_path ?? (await which("python3"));
      await run$`cd ${packagelocation}`;
      await run$`${python_path} ${packagelocation}/sveltekit_python_vercel/build.py --root ${config.root}`;

      // check if env var starts with http
      let httpPrefix = "";
      if (!loadEnv("", config.root, "").VERCEL_URL.startsWith("http")) {
        httpPrefix = "https://";
      }

      const api_url = path.join(
        httpPrefix + loadEnv("", config.root, "").VERCEL_URL
      );

      // get current Vercel deploy URL
      sveltekit_url = new URL(api_url);

      console.log("Build API URL: " + sveltekit_url.toString());
    },
  };

  const plugin_py_server_endpoint_serve: Plugin = {
    name: "vite-plugin-sveltekit_python-server-endpoint",
    apply: "serve",
    transform(src, id) {
      // console.log("Transform function called for", id); // Add this line
      if (/\.py$/.test(id)) {
        if (sveltekit_url === undefined)
          throw new Error(
            `${plugin_python_serve.name} failed to produce a sveltekit_url`
          );

        return {
          code: get_pyServerEndpointAsString(sveltekit_url, true),
          map: null, // provide source map if available
        };
      }
    },
  };

  const plugin_py_server_endpoint_build: Plugin = {
    name: "vite-plugin-sveltekit_python-server-endpoint",
    apply: "build",
    transform(src, id) {
      // console.log("Transform function called for", id); // Add this line
      if (/\.py$/.test(id)) {
        if (sveltekit_url === undefined)
          throw new Error(
            `${plugin_python_serve.name} failed to produce a sveltekit_url`
          );

        return {
          code: get_pyServerEndpointAsString(sveltekit_url, false),
          map: null, // provide source map if available
        };
      }
    },
  };

  return [
    plugin_python_serve,
    plugin_python_build,
    plugin_py_server_endpoint_serve,
    plugin_py_server_endpoint_build,
  ];
}
