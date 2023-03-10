import uuid
from typing import Optional

from databases import Database
from fastapi import Depends, status
from httpx import AsyncClient

from src.core.config import settings
from src.db.postgres import get_postgres
from src.db.request import get_request
from src.models.subscription import Subscription


class SubscriptionService:
    """Сервис взаимодействия с подписками"""

    def __init__(self, postgres: Database, request: AsyncClient):
        self.postgres = postgres
        self.request = request

    async def get_subscriptions(self) -> list[Subscription]:
        """
        Получить все подписки

        :return: список подписок
        """

        query = Subscription.select()
        return await self.postgres.fetch_all(query)

    async def get_paid_subscriptions(self) -> list[Subscription]:
        """
        Получить все платные подписки

        :return: список подписок
        """

        query = Subscription.select().filter(Subscription.c.price > 0)
        return await self.postgres.fetch_all(query)

    async def get_trial_subscription(self) -> Subscription:
        """
        Получить пробную подписки

        :return: пробная подписок
        """

        query = Subscription.select().filter(Subscription.c.price == 0)
        return await self.postgres.fetch_one(query)

    async def get_subscription_by_id(self, subs_id: uuid.UUID) -> Subscription:
        """
        Получение подписки по ее id

        :param subs_id: id подписки
        :return: подписка
        """

        query = Subscription.select().filter(Subscription.c.id == subs_id)
        return await self.postgres.fetch_one(query)

    async def mark_trial_subscription_as_used(self, subs: Subscription, user_id: uuid.UUID) -> Optional[str]:
        """
        Отметить пробную подписку как использованную пользователем user_id

        :param subs: пробная подписка
        :param user_id: id пользователя
        :return: ошибка, если есть
        """

        response = await self.request.put(
            url=f'{settings.auth_api_url}/user/{user_id}/subscriptions',
            data={
                'trial_used': True,
                'months': subs.months
            }
        )
        if response.status_code != status.HTTP_200_OK:
            return response.text


def get_subscription_service(
        postgres: Database = Depends(get_postgres),
        request: AsyncClient = Depends(get_request)
) -> SubscriptionService:
    """
    Провайдер SubscriptionService,
    с помощью Depends он сообщает, что ему необходимы Database и AsyncClient
    """
    return SubscriptionService(postgres, request)
