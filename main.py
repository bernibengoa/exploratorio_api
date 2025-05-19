from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from enum import Enum
import os
app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "¡Hola, la API está funcionando!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class RegionesChile(str, Enum):
    arica_parinacota = "Arica y Parinacota"
    tarapaca = "Tarapacá"
    antofagasta = "Antofagasta"
    atacama = "Atacama"
    coquimbo = "Coquimbo"
    valparaiso = "Valparaíso"
    metropolitana = "Metropolitana"
    ohiggins = "O'Higgins"
    maule = "Maule"
    biobio = "Biobío"
    araucania = "Araucanía"
    los_rios = "Los Ríos"
    los_lagos = "Los Lagos"
    aysen = "Aysén"
    magallanes = "Magallanes"

FACTORES_REGION = {
    RegionesChile.arica_parinacota: 1.0,       # Máxima radiación (Desierto de Atacama)
    RegionesChile.antofagasta: 0.95,
    RegionesChile.atacama: 0.9,
    RegionesChile.coquimbo: 0.85,
    RegionesChile.valparaiso: 0.8,
    RegionesChile.metropolitana: 0.75,
    RegionesChile.ohiggins: 0.7,
    RegionesChile.maule: 0.65,
    RegionesChile.biobio: 0.6,
    RegionesChile.araucania: 0.55,
    RegionesChile.los_rios: 0.5,
    RegionesChile.los_lagos: 0.45,
    RegionesChile.aysen: 0.4,
    RegionesChile.magallanes: 0.35             # Mínima radiación
}
    
# Modelo de entrada para huella de carbono
class CarbonFootprintInput(BaseModel):
    km_por_semana: float  # kilómetros en auto por semana
    consumo_energetico_kwh_mes: float  # consumo eléctrico mensual (kWh)


# Modelo de entrada para ahorro con paneles solares
class SolarSavingsInput(BaseModel):
    consumo_kwh_mensual: float
    region: RegionesChile 
    costo_kwh: float = 150  # pesos chilenos por defecto por kWh
    porcentaje_cubierto: float = Field(default=None, exclude=True) 


@app.post("/huella-carbono")
def calcular_huella(data: CarbonFootprintInput):
    # Factores aproximados:
    # - 0.21 kg CO2 por km en auto
    # - 0.4 kg CO2 por kWh consumido
    huella_auto = data.km_por_semana * 0.21 * 4
    huella_electricidad = data.consumo_energetico_kwh_mes * 0.4

    total = huella_auto + huella_electricidad
    return {
        "huella_auto_kg": round(huella_auto, 2),
        "huella_electricidad_kg": round(huella_electricidad, 2),
        "huella_total_kg": round(total, 2),
    }
    
@app.post("/ahorro-paneles")
def calcular_ahorro(data: SolarSavingsInput):
    factor_region = FACTORES_REGION[data.region]
    porcentaje_efectivo = 0.8 * factor_region 
    energia_generada = data.consumo_kwh_mensual * porcentaje_efectivo
    ahorro_mensual = energia_generada 
    ahorro_anual = ahorro_mensual * 12
    return {
        "region": data.region.value,
        "factor_radiacion": factor_region,
        "porcentaje_efectivo": round(porcentaje_efectivo * 100, 1),
        "kwh_generados_mensuales": round(energia_generada, 1),
        "ahorro_mensual_CLP": round(ahorro_mensual, 1),
        "ahorro_anual_CLP": round(ahorro_anual, 1),
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
