from enum import Enum


class ClientType(Enum):
    INDIVIDUAL = "Particular"
    SMALL_BUSINESS = "Pequena Empresa"
    CORPORATE = "Corporativo"
    ENTERPRISE = "Grande Empresa"
    GOVERNMENT = "Governo"
    NON_PROFIT = "Organização Sem Fins Lucrativos"
    DISTRIBUTOR = "Distribuidor"
    RESELLER = "Revendedor"
    SERVICE_PROVIDER = "Prestador de Serviços"


class SupplierType(Enum):
    RAW_MATERIAL_SUPPLIER = "Fornecedor de Matérias-Primas"
    COMPONENT_SUPPLIER = "Fornecedor de Componentes"
    CONSUMABLE_SUPPLIER = "Fornecedor de Consumíveis"
    PACKAGING_SUPPLIER = "Fornecedor de Embalagens"
    SPARE_PARTS_SUPPLIER = "Fornecedor de Peças de Substituição"
    LOGISTICS_PROVIDER = "Prestador de Serviços Logísticos"
    MAINTENANCE_SUPPLIER = "Fornecedor de Serviços de Manutenção"
    TECHNOLOGY_SUPPLIER = "Fornecedor de Tecnologia"
    ENERGY_SUPPLIER = "Fornecedor de Energia"


class ProductCategory(Enum):
    FINISHED_GOODS = "Produtos Acabados"
    SEMI_FINISHED_GOODS = "Productos Semi-Acabados"
    CUSTOM_PRODUCTS = "Produtos Personalizados"
    STANDARD_PRODUCTS = "Produtos Normalizados"
    KITS_AND_ASSEMBLIES = "Kits e Conjuntos"
    DIGITAL_PRODUCTS = "Produtos Digitais"
    SERVICES = "Serviços"
    BY_PRODUCTS = "Subprodutos"
    CO_PRODUCTS = "Coprodutos"


class MaterialCategory(Enum):
    RAW_MATERIAL = "Matéria-prima"
    COMPONENT = "Componente"
    CONSUMABLE = "Consumível"
    PACKAGING_MATERIAL = "Material de Embalagem"
    SPARE_PART = "Peça de Substituição"
    AUXILIARY_MATERIAL = "Material Auxiliar"
    CHEMICAL_MATERIAL = "Material Químico"
    ELECTRONIC_MATERIAL = "Material Eletrónico"
    MECHANICAL_MATERIAL = "Material Mecânico"
