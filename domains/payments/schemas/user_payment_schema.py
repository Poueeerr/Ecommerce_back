import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from domains.payments.payments_enums import PaymentsStatus


class UserPaymentResponse(BaseModel):
    order_id: uuid.UUID
    total: Decimal
    status: PaymentsStatus
    checkout_url: str | None
    created_at: datetime
