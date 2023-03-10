from dataclasses import dataclass

from fastapi import Query, Path
from pydantic import Required


@dataclass
class Params:
    """
    Класс параметров запроса API
    """

    user_id: Query = Query(
        default=Required,
        title="Id пользователя"
    )

    promo_code: Query = Query(
        default=Required,
        title="Код промокода"
    )

    promo_id: Path = Path(
        default=Required,
        title="UUID промокода"
    )

    subs_id: Query = Query(
        default=Required,
        title="UUID подписки"
    )

    discount_id: Path = Path(
        default=Required,
        title="UUID скидки"
    )

    film_id: Query = Query(
        default=Required,
        title='UUID фильма'
    )


params = Params()
