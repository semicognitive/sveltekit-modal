import { loadEnv, type Plugin } from 'vite'
import { type ProcessPromise, $ as run$, cd as cd$, chalk } from "zx";
import globsync from "rollup-plugin-globsync";

const get_pyServerEndpointAsString = (modal_url: URL) => `
    const handle = (method) => (async ({ request, fetch, url }) => {
        const headers = new Headers()
        headers.append('content-type', request.headers.get('content-type'));
        headers.append('accept', request.headers.get('accept'));
    
        return fetch(new URL(url.pathname + '?', new URL('${modal_url}')) + url.search, { headers, method, body: request.body, signal: request.signal, duplex: 'half' })
    });
    
    export const GET = handle('GET');
    export const POST = handle('POST');
    export const PATCH = handle('PATCH');
    export const PUT = handle('PUT');
    export const DELETE = handle('DELETE');
`;

export async function sveltekit_modal(): Promise<Plugin[]> {
    const child_processes: ProcessPromise[] = [];
    async function kill_all_process() {
        for (const ps of child_processes) {
            await ps.kill();
            await ps.exitCode;
        }
    }

    let modal_url: URL | undefined;

    const plugin_glob_sync: Plugin = globsync({
        globs: [
            "src/routes/**/*.py",
            'sveltekit_modal_config.py',
        ],
        dest: './node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal',
        clean: true,
        clean_globs: [
            './node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/**/*',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/__init__.py',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/app.py',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/config.py',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/pyproject.toml',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/deploy.py',
            '!./node_modules/sveltekit-modal/esm/src/vite/sveltekit_modal/server.py',
        ]
    });

    const plugin_modal_serve: Plugin = {
        name: 'vite-plugin-sveltekit-modal-serve',
        apply: 'serve',
        async closeBundle() {
            await kill_all_process();
        },
        async configureServer({ config }) {
            run$.verbose = false;
            run$.env.PYTHONDONTWRITEBYTECODE = '1';

            cd$(packagelocation)

            const local_process: ProcessPromise = run$`python3 -m sveltekit_modal.serve`;
            child_processes.push(local_process);

            cd$(config.root)

            local_process.quiet();
            local_process.nothrow();

            local_process.stderr.on("data", (s) => {
                console.log(s.toString().trimEnd()) //Logs stderr always and all of stdout if 'log': True
            });
            local_process.stderr.on("error", (s) => {
                console.error(chalk.red('Error: Modal Serve Failed'))
                console.error(s.toString().trimEnd())
            });
            local_process.stdout.on("data", (s) => {
                const out = s.toString().trimEnd();

                const modal_route_match = out.match(/https:\/\/.*?\.modal\.run/)?.toString();
                if (modal_route_match) modal_url ??= new URL(modal_route_match);
            });
            local_process.stdout.on("error", (s) => {
                console.error(chalk.red('Error: Modal Serve Failed'))
                console.error(s.toString().trimEnd())
            });
        },
    };


    const plugin_modal_build: Plugin = {
        name: 'vite-plugin-sveltekit-modal-build',
        apply: 'build',
        configResolved(config) {
            modal_url = new URL(loadEnv('production', config.root, "").MODAL_APP_URL)
        },
    };

    const plugin_py_server_endpoint: Plugin = {
        name: 'vite-plugin-sveltekit-modal-py-server-endpoint',
        transform(src, id) {
            if (/\.py$/.test(id)) {
                if (modal_url === undefined) throw new Error(`${plugin_modal_serve.name} failed to produce a modal_url`)

                return {
                    code: get_pyServerEndpointAsString(modal_url),
                    map: null, // provide source map if available
                }
            }
        },
    };

    return [plugin_glob_sync, plugin_modal_serve, plugin_modal_build, plugin_py_server_endpoint];
};
