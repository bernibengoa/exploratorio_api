from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"mensaje": "¡Hola, la API está funcionando!"}
    
# Modelo de entrada para huella de carbono
class CarbonFootprintInput(BaseModel):
    km_por_semana: float  # kilómetros en auto por semana
    consumo_energetico_kwh_mes: float  # consumo eléctrico mensual (kWh)


# Modelo de entrada para ahorro con paneles solares
class SolarSavingsInput(BaseModel):
    consumo_kwh_mensual: float
    costo_kwh: float = 150  # pesos chilenos por defecto por kWh
    porcentaje_cubierto: float = 0.8  # paneles cubren el 80% del consumo


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
    energia_generada = data.consumo_kwh_mensual * data.porcentaje_cubierto
    ahorro_mensual = energia_generada * data.costo_kwh
    ahorro_anual = ahorro_mensual * 12
    return {
        "kwh_generados_mensuales": round(energia_generada, 1),
        "ahorro_mensual_CLP": round(ahorro_mensual, 1),
        "ahorro_anual_CLP": round(ahorro_anual, 1),
    }
# Flask (Python)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

