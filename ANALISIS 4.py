# ============================================================
# DESCOMPOSICIÓN ESTRUCTURAL DEL EMPLEO + AGREGACIÓN SECTORIAL
# ============================================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ruta = r"D:\GAMER LAPTOP\Desktop\Articulos finalizados\DYLAN ARTICULO\\"

# ========================
# CARGA DE DATOS
# ========================

L0 = pd.read_excel(ruta + 'Leontief_2013.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values
L1 = pd.read_excel(ruta + 'Leontief_2023.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values

f0 = pd.read_excel(ruta + 'DemandaFinal_2013.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values
f1 = pd.read_excel(ruta + 'DemandaFinal_2023.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values

e0 = pd.read_excel(ruta + 'CoefEmpleo_2013.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()
e1 = pd.read_excel(ruta + 'CoefEmpleo_2023.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()

L0 = np.nan_to_num(L0)
L1 = np.nan_to_num(L1)
f0 = np.nan_to_num(f0)
f1 = np.nan_to_num(f1)
e0 = np.nan_to_num(e0)
e1 = np.nan_to_num(e1)

# ========================
# DESCOMPOSICIÓN SDA
# ========================

Ehat0 = np.diag(e0)
Ehat1 = np.diag(e1)

dEhat = Ehat1 - Ehat0
dL = L1 - L0
df = f1 - f0

Effect_Intensity = 0.5 * dEhat @ (L0 @ f0 + L1 @ f1)
Effect_Technology = 0.5 * (Ehat0 @ dL @ f1 + Ehat1 @ dL @ f0)
Effect_Demand = 0.5 * (Ehat0 @ L0 + Ehat1 @ L1) @ df

Total_Change = Effect_Intensity + Effect_Technology + Effect_Demand

# ========================
# RESULTADOS POR SECTOR
# ========================

resultados = pd.DataFrame({
    'Sector': np.arange(1, len(Total_Change)+1),
    'Efecto_Intensidad': Effect_Intensity.flatten(),
    'Efecto_Tecnologia': Effect_Technology.flatten(),
    'Efecto_Demanda': Effect_Demand.flatten(),
    'Cambio_Total_Empleo': Total_Change.flatten()
})

resultados.to_excel(ruta + "Resultados_SDA_2013_2023.xlsx", index=False)

# ========================
# AGREGACIÓN ESTRUCTURAL
# ========================

grupos = {
    "Primario": list(range(1,10)),
    "Industria": list(range(10,34)),
    "Transporte": [49,50,51,52,53],
    "Residencial": [55,56]
}

agregado = []

for nombre, sectores in grupos.items():
    df_g = resultados[resultados["Sector"].isin(sectores)]
    agregado.append([
        nombre,
        df_g["Efecto_Intensidad"].sum(),
        df_g["Efecto_Tecnologia"].sum(),
        df_g["Efecto_Demanda"].sum(),
        df_g["Cambio_Total_Empleo"].sum()
    ])

usados = sum(grupos.values(), [])
otras = resultados[~resultados["Sector"].isin(usados)]

agregado.append([
    "Otras",
    otras["Efecto_Intensidad"].sum(),
    otras["Efecto_Tecnologia"].sum(),
    otras["Efecto_Demanda"].sum(),
    otras["Cambio_Total_Empleo"].sum()
])

agregado_df = pd.DataFrame(agregado, columns=[
    "Bloque", "Intensidad", "Tecnologia", "Demanda", "Cambio_Total"
])

agregado_df.to_excel(ruta + "Agregacion_Estructural_Empleo.xlsx", index=False)

# ========================
# GRÁFICO ESTRUCTURAL 
# ========================

fig, ax = plt.subplots(figsize=(9,5))

ax.bar(agregado_df["Bloque"], agregado_df["Intensidad"], label="Intensidad", edgecolor='none')
ax.bar(agregado_df["Bloque"], agregado_df["Tecnologia"],
       bottom=agregado_df["Intensidad"], label="Tecnología", edgecolor='none')
ax.bar(agregado_df["Bloque"], agregado_df["Demanda"],
       bottom=agregado_df["Intensidad"] + agregado_df["Tecnologia"],
       label="Demanda", edgecolor='none')

ax.set_title("Descomposición estructural del empleo por bloques productivos (2013–2023)")
ax.set_ylabel("Variación del empleo")
ax.legend(frameon=False)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()

print("Proceso completo finalizado")
