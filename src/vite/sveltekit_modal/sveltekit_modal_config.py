import modal
import sveltekit_modal

config: sveltekit_modal.Config = {
    'log': False,
    'stub_asgi': {
        'image': modal.Image.debian_slim()
    }
}