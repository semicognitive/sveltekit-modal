import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

import { sveltekit_modal } from "sveltekit-modal/vite"; //Add this import

export default defineConfig({
  plugins: [sveltekit_modal(), sveltekit()],
});
