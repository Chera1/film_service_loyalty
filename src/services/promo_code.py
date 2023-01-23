import uuid

from typing import Optional, Union, Tuple

from aioredis import Redis
from fastapi import Depends, Request, Query

from src.services.views import Views
from src.db.redis import get_redis
from src.models.promo_code import PromoCode, BasePromoApi
from src.utils.cache import AbstractCache, RedisCache
# from src.utils.sort_string import clear_sort_string


class PromoService(Views):
    def __init__(self, cache: AbstractCache):
        self.cache = cache

    async def get_promo_by_id(self, promo_id: uuid.UUID) -> Optional[PromoCode]:
        """
        Получаем промокод по uuid

        @param promo_id: uuid промокода
        @return: объект-промокод
        """
        promo = await self.get_record_by_id(promo_id)
        return PromoCode(**promo) if promo else None

    async def create_promo(self, data: dict) -> Optional[BasePromoApi]:
        """
        Получаем промокод по uuid

        @param data: объект промокода
        @return: объект-промокод
        """
        promo = await self.set_record_to_redis(data)
        return BasePromoApi(**promo) if promo else None

    # async def get_films(
    #         self,
    #         sort: Optional[str] = None,
    #         limit: Optional[int] = 50,
    #         page: Optional[int] = 1,
    #         genre: Optional[Union[uuid.UUID, list[uuid.UUID], None]] = Query(default=None),
    #         query: Optional[str] = None
    # ) -> Tuple[Union[list[Film], None], list[str]]:
    #     """
    #     Получает список фильмов
    #
    #     @param sort: имя поля по которому идет сортировка
    #     @param limit: количество записей на странице
    #     @param page: номер страницы
    #     @param genre: uuid-жанра для фильтрации
    #     @param query: поисковый запрос
    #     @return: Данные по фильмам
    #     """
    #
    #     errors = []
    #     query_ = None
    #
    #     films = await self.cache.get()
    #
    #     if not films:
    #         sort = clear_sort_string(sort, 'title')
    #
    #         if genre:
    #             # если в запросе есть параметр genre - добавляем запрос
    #             if isinstance(genre, uuid.UUID):
    #                 genre = [str(genre)]
    #
    #             genre_query = [
    #                 {"term": {"genre.id": str(one_genre)}}
    #                 for one_genre in genre
    #             ]
    #
    #             query_ = {
    #                 "query": {
    #                     "nested": {
    #                         "path": "genre",
    #                         "query": {
    #                             "bool": {
    #                                 "should": genre_query
    #                             }
    #                         }
    #                     }
    #                 }
    #             }
    #
    #         if query:
    #             # если в запросе есть параметр query - добавляем запрос на поиск
    #             query_ = {
    #                 "query": {
    #                     "match": {
    #                         "title": {
    #                             "query": query,
    #                             "fuzziness": "auto"
    #                         }
    #                     }
    #                 }
    #             }
    #
    #         try:
    #             films = await self.elastic.search(
    #                 index='movies',
    #                 body=query_,
    #                 size=limit,
    #                 sort=sort,
    #                 page=page
    #             )
    #
    #             await self.cache.set(films)
    #
    #         except RequestError:
    #             films = None
    #             errors.append('В запрашиваемых параметрах содержатся ошибки')
    #
    #     return films, errors
    #
    # async def get_same_films(
    #         self,
    #         film_id: uuid.UUID,
    #         sort: Optional[str] = None,
    #         limit: Optional[int] = 50,
    #         page: Optional[int] = 1,
    # ) -> Tuple[Union[list[Film], None], list[str]]:
    #     try:
    #         film = await self.elastic.get('movies', film_id)
    #
    #         genre = [
    #             genre['id']
    #             for genre in film['_source']['genre']
    #         ]
    #
    #     except NotFoundError:
    #         return None
    #
    #     result = await self.get_films(
    #         sort=sort,
    #         limit=limit,
    #         page=page,
    #         genre=genre
    #     )
    #
    #     return result


def get_promo_service(
        request: Request,
        redis: Redis = Depends(get_redis),
) -> PromoService:
    """
    Провайдер FilmService,
    с помощью Depends он сообщает, что ему необходимы Redis
    """
    return PromoService(RedisCache(redis, request))
