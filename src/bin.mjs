#!/usr/bin/env zx --install

import 'zx/globals';

import { parse, stringify } from 'envfile';

const cmd = argv._[0];
switch (cmd) {
    case "deploy":
        $.verbose = true;
        $.env.PYTHONDONTWRITEBYTECODE = '1';

        $.log = (entry) => {
            if (entry.kind == 'stdout' || entry.kind == 'stderr') log(entry)
            else return
        }

        cd(path.join('.', 'node_modules', 'sveltekit-modal', 'esm/src/vite'))

        const deploy_log = await $`python3 -m sveltekit_modal.deploy`;
        const modal_route_match = deploy_log.stdout.match(/https:\/\/.*?\.modal\.run/)?.toString();

        cd(path.join('..', '..', '..', '../../..'))

        await fs.ensureFile('.env.production')

        const env_prod = await fs.readFile('.env.production', 'utf-8').then(parse);
        await fs.writeFile('.env.production', stringify({ ...env_prod, MODAL_APP_URL: modal_route_match }));
        break;
    default:
        echo`Invalid command ${cmd}. Did you mean "deploy"?`
        break;
}