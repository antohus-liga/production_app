from dataclasses import dataclass, field
import datetime
from decimal import Decimal


@dataclass(frozen=True)
class MovementInRecord:
    nr: int
    mat_code: str
    sup_code: str
    quantity: int
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class MovementInView(MovementInRecord):
    total_price: Decimal = Decimal("0.00")
