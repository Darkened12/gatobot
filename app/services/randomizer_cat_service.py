import random
from app.controllers.gifs_controller import GifsController

_EMOJIS: list[str] = ['<:gato:1180027630871904276>',
                      '<:gatodespair:1280387632492449946>', ]


async def get_random_cat(controller: GifsController) -> str:
    gif = await controller.get_random_gif()
    if gif is not None:
        return random.choices(
            _EMOJIS + gif,
            weights=[20, 20, gif.weight],
            k=1
        )[0]
    return random.choice(_EMOJIS)
