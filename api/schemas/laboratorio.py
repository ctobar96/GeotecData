# El Esquema de Validación (Pydantic)
from pydantic import BaseModel, Field

class AtterbergRequest(BaseModel):
    limite_liquido: float = Field(..., gt=0, description="Límite Líquido (LL) en %")
    limite_plastico: float = Field(..., gt=0, description="Límite Plástico (LP) en %")

class AtterbergResponse(BaseModel):
    limite_liquido: float
    limite_plastico: float
    indice_plasticidad: float
    clasificacion_casagrande: str
    estado_consistencia: str