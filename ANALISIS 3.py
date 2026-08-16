import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ruta = r"D:\GAMER LAPTOP\Desktop\Articulos finalizados\DYLAN ARTICULO\\"

# ========================
# CARGA DESDE EXCEL
# ========================

L0 = pd.read_excel(ruta + 'Leontief_2013.xlsx', header=None)
L1 = pd.read_excel(ruta + 'Leontief_2023.xlsx', header=None)

# Conversión forzada a numérico
L0 = L0.apply(pd.to_numeric, errors='coerce').values
L1 = L1.apply(pd.to_numeric, errors='coerce').values


f0 = pd.read_excel(ruta + 'DemandaFinal_2013.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values
f1 = pd.read_excel(ruta + 'DemandaFinal_2023.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values

e0 = pd.read_excel(ruta + 'CoefEmpleo_2013.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()
e1 = pd.read_excel(ruta + 'CoefEmpleo_2023.xlsx', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()



# ========================
# LIMPIEZA NUMÉRICA
# ========================

L0 = np.nan_to_num(L0)
L1 = np.nan_to_num(L1)
f0 = np.nan_to_num(f0)
f1 = np.nan_to_num(f1)
e0 = np.nan_to_num(e0)
e1 = np.nan_to_num(e1)

# ========================
# MODELO SDA EXACTO
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
# RESULTADOS
# ========================

resultados = pd.DataFrame({
    'Sector': np.arange(1, len(Total_Change)+1),
    'Efecto_Intensidad': Effect_Intensity.flatten(),
    'Efecto_Tecnologia': Effect_Technology.flatten(),
    'Efecto_Demanda': Effect_Demand.flatten(),
    'Cambio_Total_Empleo': Total_Change.flatten()
})

print(resultados)



# ========================
# DESCOMPOSICIÓN AGREGADA
# ========================

agregado = resultados[['Efecto_Intensidad','Efecto_Tecnologia','Efecto_Demanda']].sum()
agregado.index = ['Efecto Intensidad', 'Efecto Tecnología', 'Efecto Demanda']

fig, ax = plt.subplots(figsize=(8,5))   

ax.bar(agregado.index, agregado.values, edgecolor='none')

ax.set_title('Descomposición estructural del cambio del empleo (2013–2023)')
ax.set_xlabel('Componentes')
ax.set_ylabel('Variación del empleo')

# Eliminar todo contorno
for spine in ax.spines.values():
    spine.set_visible(False)

ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()

#ACUMULADO

acumulado = agregado.cumsum()

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(agregado.index, agregado.values, edgecolor='none')
ax.plot(agregado.index, acumulado.values, marker='o')

ax.set_title("Contribución estructural al cambio del empleo (2013–2023)")
ax.set_xlabel("Componentes")
ax.set_ylabel("Empleo acumulado")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()


#CONTRIBUCION ESTRUCTURAL AGREGADA
valores = agregado.values
etiquetas = agregado.index

acum = [0]
for v in valores:
    acum.append(acum[-1] + v)

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(etiquetas, valores, bottom=acum[:-1], edgecolor='none')
ax.plot([etiquetas[0], etiquetas[-1]], [0, acum[-1]], marker='o')

ax.set_title("Contribución estructural al cambio del empleo")
ax.set_ylabel("Empleo")

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()

#Composición del cambio del empleo por sector (apilado, limpio)
fig, ax = plt.subplots(figsize=(11,5))

# Barras apiladas con etiquetas para la leyenda
ax.bar(resultados['Sector'], resultados['Efecto_Intensidad'],
       label='Efecto Intensidad', edgecolor='none')

ax.bar(resultados['Sector'], resultados['Efecto_Tecnologia'],
       bottom=resultados['Efecto_Intensidad'],
       label='Efecto Tecnología', edgecolor='none')

ax.bar(resultados['Sector'], resultados['Efecto_Demanda'],
       bottom=resultados['Efecto_Intensidad'] + resultados['Efecto_Tecnologia'],
       label='Efecto Demanda', edgecolor='none')

# Títulos y ejes
ax.set_title("Composición del cambio del empleo por sector")
ax.set_xlabel("Sector")
ax.set_ylabel("Empleo")

# Leyenda que explica los colores
ax.legend(frameon=False)


for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()


# SECTOR 48

s48 = resultados[resultados["Sector"] == 48].iloc[0]

values = [s48["Efecto_Intensidad"], s48["Efecto_Tecnologia"], s48["Efecto_Demanda"]]
labels = ["Intensidad", "Tecnología", "Demanda"]

# Cálculo acumulado para cascada
cum = [0]
for v in values:
    cum.append(cum[-1] + v)

fig, ax = plt.subplots(figsize=(7,5))

bars = ax.bar(labels, values, bottom=cum[:-1], edgecolor='none')
ax.plot(["Intensidad","Demanda"], [0, cum[-1]], marker='o')

# ====== ETIQUETAS NUMÉRICAS ======
for bar, v, base in zip(bars, values, cum[:-1]):
    ax.text(bar.get_x() + bar.get_width()/2,
            base + v/2,
            f"{v:,.0f}",
            ha='center', va='center', fontsize=10)

# ====== TÍTULOS Y EJES ======
ax.set_title("Descomposición del cambio del empleo – Sector eléctrico (48)")
ax.set_ylabel("Variación del empleo")

# ====== LEYENDA EXPLICATIVA ======
ax.legend(
    ["Trayectoria acumulada", "Efecto estructural"],
    loc="upper left",
    frameon=False
)

# ====== ESTILO LIMPIO ======
for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(axis='both', length=0)

plt.tight_layout()
plt.show()



# ========================
# EXPORTAR RESULTADOS
# ========================

archivo_excel = ruta + "Resultados_SDA_2013_2023.xlsx"

with pd.ExcelWriter(archivo_excel, engine="openpyxl") as writer:
    resultados.to_excel(writer, sheet_name="Resultados_SDA", index=False)

print("Archivo Excel creado correctamente en:")
print(archivo_excel)
