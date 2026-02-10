from dataclasses import dataclass, field
from decimal import Decimal
import datetime

from models.enums import BaseUnit, ProductCategory


@dataclass
class Product:
    code: str
    name: str
    category: ProductCategory
    base_unit: BaseUnit
    unit_price: Decimal
    quantity: int = field(init=False, default=0)
    production_cost: Decimal = field(init=False, default=Decimal("0.00"))
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)
