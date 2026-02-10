from dataclasses import dataclass, field
import datetime
from decimal import Decimal


@dataclass(frozen=True)
class ProductionLineRecord:
    nr: int
    pro_code: str
    quantity: int
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class ProductionLineView(ProductionLineRecord):
    total_cost: Decimal = Decimal("0.00")
