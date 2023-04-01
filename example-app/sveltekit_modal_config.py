import modal

config = {
    'name': 'sveltekit-example',
    'log': False,
    'stub_asgi': {
        'image': modal.Image.debian_slim()
    }
}