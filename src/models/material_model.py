from dataclasses import dataclass, field
from decimal import Decimal
import datetime

from models.enums import BaseUnit, MaterialCategory


@dataclass(frozen=True)
class MaterialRecord:
    code: str
    name: str
    category: MaterialCategory
    base_unit: BaseUnit
    unit_price: Decimal
    quantity: int = field(init=False, default=0)
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)


@dataclass(frozen=True)
class MaterialView(MaterialRecord):
    quantity: int = 0
