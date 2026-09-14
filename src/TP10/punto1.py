import numpy as np
import numpy_financial as npf

# ==========================================
# DATOS INICIALES DEL PROBLEMA
# ==========================================
tasa = 0.01                 # Tasa efectiva mensual (1%)
inversion_mensual = -1000   # Costo mensual de inversión (egreso)
valor_subyacente = 18000    # Ingreso por negocio subyacente en el mes de finalización

print("--- RESULTADOS FINANCIEROS DEL PROYECTO ---\n")

# ==========================================
# a. VPN del proyecto según planes (12 meses)
# ==========================================
flujos_plan = [0] + [inversion_mensual] * 11 + [inversion_mensual + valor_subyacente]
npv_plan = npf.npv(tasa, flujos_plan)
print(f"a) NPV según los planes (12 meses): ${npv_plan:,.2f}")

# ==========================================
# b. VPN del proyecto extendido 3 meses más (15 meses)
# ==========================================
flujos_ext = [0] + [inversion_mensual] * 14 + [inversion_mensual + valor_subyacente]
npv_ext = npf.npv(tasa, flujos_ext)
print(f"b) NPV con extensión de 3 meses (15 meses): ${npv_ext:,.2f}")

# ==========================================
# c. Rentabilidad (NPV / Valor Presente de la Inversión)
# ==========================================
vp_inv_plan = sum([inv / (1 + tasa)**i for i, inv in enumerate([0] + [inversion_mensual]*12)])
rentabilidad_plan = npv_plan / abs(vp_inv_plan)

vp_inv_ext = sum([inv / (1 + tasa)**i for i, inv in enumerate([0] + [inversion_mensual]*15)])
rentabilidad_ext = npv_ext / abs(vp_inv_ext)

print(f"c) Rentabilidad del caso a) (12 meses): {rentabilidad_plan * 100:.2f}%")
print(f"   Rentabilidad del caso b) (15 meses): {rentabilidad_ext * 100:.2f}%")

# ==========================================
# f. [Desafío] Costo mensual máximo aceptable (15 meses)
# ==========================================
meta_npv = npv_plan

def calcular_npv_con_costo(c_mensual):
    flujos_c = [0] + [-c_mensual] * 15
    flujos_c[15] += valor_subyacente
    return npf.npv(tasa, flujos_c)

costos_prueba = np.linspace(500, 2000, 15000)
costo_maximo = max([c for c in costos_prueba if calcular_npv_con_costo(c) >= meta_npv])

print(f"\nf) [Desafío] Costo mensual máximo aceptable (15 meses): ${costo_maximo:,.2f}")