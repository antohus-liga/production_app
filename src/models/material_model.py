from dataclasses import dataclass, field
from decimal import Decimal
import datetime

from models.enums import BaseUnit, MaterialCategory


@dataclass
class Material:
    code: str
    name: str
    category: MaterialCategory
    base_unit: BaseUnit
    unit_price: Decimal
    quantity: int = field(init=False, default=0)
    created_at: datetime.date = field(default_factory=datetime.date.today)
    updated_at: datetime.date = field(default_factory=datetime.date.today)
