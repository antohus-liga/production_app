from dataclasses import dataclass


@dataclass(frozen=True)
class ProductMaterials:
    nr: int
    pro_code: str
    mat_code: str
    quantity: int
