from dataclasses import dataclass, field
from decimal import Decimal
import datetime

from models.enums import BaseUnit, ProductCategory


@dataclass(frozen=True)
class ProductRecord:
    code: str
    name: str
    category: ProductCategory
    base_unit: BaseUnit
    unit_price: Decimal
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class ProductView(ProductRecord):
    quantity: int = 0
    production_cost: Decimal = Decimal("0.00")
