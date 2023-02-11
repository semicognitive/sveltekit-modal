#!/usr/bin/env zx

import 'zx/globals';

import { parse, stringify } from 'envfile';

const cmd = process.argv[3];
switch (cmd) {
    case "deploy":
        $.verbose = true;
        $.env.PYTHONDONTWRITEBYTECODE = '1';

        $.log = (entry) => {
            if (entry.kind == 'stdout' || entry.kind == 'stderr') log(entry)
            else return
        }

        cd('src/lib/vite')

        const deploy_log = await $`python3 sveltekit_modal_deploy.py`;
        const modal_route_match = deploy_log.stdout.match(/https:\/\/.*?\.modal\.run/)?.toString();

        cd('../../..')

        await fs.ensureFile('.env.production')

        const env_prod = await fs.readFile('.env.production', 'utf-8').then(parse);
        await fs.writeFile('.env.production', stringify({ ...env_prod, MODAL_APP_URL: modal_route_match }));
        break;
    default:
        echo`Invalid command ${cmd}. Did you mean "deploy"?`
        break;
}