import random
from app.controllers.gifs_controller import GifsController

_EMOJIS: list[str] = ['<:gato:1180027630871904276>',
                      '<:gatodespair:1280387632492449946>', ]


async def get_random_cat(controller: GifsController) -> str:
    gif = await controller.get_random_gif()
    if gif is not None:
        result = _EMOJIS.copy()
        result.append(gif.url)
        return random.choices(
            result,
            weights=[20, 20, gif.weight],
            k=1
        )[0]
    return random.choice(_EMOJIS)
