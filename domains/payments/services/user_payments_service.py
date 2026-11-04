import uuid

from domains.payments.models.payments_model import PaymentsModel
from domains.payments.repositories.payments_repository import PaymentsRepository


class UserPaymentsService:
    def __init__(self, repository: PaymentsRepository):
        self.repository = repository

    async def list_payments(self, user_id: uuid.UUID) -> list[PaymentsModel]:
        return await self.repository.list_by_user(user_id)
