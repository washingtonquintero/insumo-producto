import pandas as pd
import numpy as np
import os
print(os.getcwd())

# ======================================================
# 1. DEFINIR RUTA DE LOS ARCHIVOS
# ======================================================

ruta = r"D:\GAMER LAPTOP\Desktop\Articulos finalizados\DYLAN ARTICULO\\"

# ======================================================
# 2. CARGA Y LIMPIEZA DE DATOS
# ======================================================

L0 = pd.read_csv(ruta + 'Leontief_2013.csv', header=None, sep=';').apply(pd.to_numeric, errors='coerce').values
L1 = pd.read_csv(ruta + 'Leontief_2023.csv', header=None, sep=';').apply(pd.to_numeric, errors='coerce').values

print("L0:", L0.shape)
print("L1:", L1.shape)

# Reemplazar NaN por 0 (no altera la contabilidad estructural)
L0 = np.nan_to_num(L0, nan=0.0)
L1 = np.nan_to_num(L1, nan=0.0)


f0 = pd.read_csv(ruta + 'DemandaFinal_2013.csv', header=None).apply(pd.to_numeric, errors='coerce').values.reshape(-1,1)
f1 = pd.read_csv(ruta + 'DemandaFinal_2023.csv', header=None).apply(pd.to_numeric, errors='coerce').values.reshape(-1,1)

e0 = pd.read_csv(ruta + 'CoefEmpleo_2013.csv', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()
e1 = pd.read_csv(ruta + 'CoefEmpleo_2023.csv', header=None).apply(pd.to_numeric, errors='coerce').values.flatten()

print(np.isnan(L0).sum(), np.isnan(L1).sum())
print(np.isnan(f0).sum(), np.isnan(f1).sum())
print(np.isnan(e0).sum(), np.isnan(e1).sum())


# ======================================================
# 3. CONSTRUCCIÓN DE MATRICES Y DIFERENCIAS
# ======================================================

Ehat0 = np.diag(e0)
Ehat1 = np.diag(e1)

dEhat = Ehat1 - Ehat0
dL = L1 - L0
df = f1 - f0

# ======================================================
# 4. DESCOMPOSICIÓN SDA EXACTA (Dietzenbacher-Los)
# ======================================================

Effect_Intensity = 0.5 * dEhat @ (L0 @ f0 + L1 @ f1)

Effect_Technology = 0.5 * (Ehat0 @ dL @ f1 + Ehat1 @ dL @ f0)

Effect_Demand = 0.5 * (Ehat0 @ L0 + Ehat1 @ L1) @ df

Total_Change = Effect_Intensity + Effect_Technology + Effect_Demand

# ======================================================
# 5. TABLA DE RESULTADOS
# ======================================================

resultados = pd.DataFrame({
    'Sector': np.arange(1, len(Total_Change) + 1),
    'Efecto_Intensidad': Effect_Intensity.flatten(),
    'Efecto_Tecnologia': Effect_Technology.flatten(),
    'Efecto_Demanda': Effect_Demand.flatten(),
    'Cambio_Total_Empleo': Total_Change.flatten()
})

print(resultados)

# ======================================================
# 6. GUARDAR RESULTADOS
# ======================================================

resultados.to_csv(ruta + 'Resultados_SDA_2013_2023.csv', index=False)
