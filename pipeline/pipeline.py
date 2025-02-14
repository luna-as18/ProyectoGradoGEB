import pandas as pd
from sklearn.preprocessing import StandardScaler

# 1️⃣ Leer los 3 archivos
file_paths = {
    "EICH101": r"C:/Users/diana/OneDrive - Universidad de los Andes/Documentos/9no Semestre/TesisGEB_AlejaYCami/Repositorio/ProyectoGradoGEB/datos/EICH101.xlsx",
    "EICH102": r"C:/Users/diana/OneDrive - Universidad de los Andes/Documentos/9no Semestre/TesisGEB_AlejaYCami/Repositorio/ProyectoGradoGEB/datos/EICH102.xlsx",
    "EICH104": r"C:/Users/diana/OneDrive - Universidad de los Andes/Documentos/9no Semestre/TesisGEB_AlejaYCami/Repositorio/ProyectoGradoGEB/datos/EICH104.xlsx"
}

# Cargar los archivos en dataframes
e1 = pd.read_excel(file_paths["EICH101"])
e2 = pd.read_excel(file_paths["EICH102"])
e3 = pd.read_excel(file_paths["EICH104"])

# 2️⃣ Filtrar registros según ORIG_RAW_VOLUME
e1 = e1[e1["ORIG_RAW_VOLUME"] <= 60]
e2 = e2[e2["ORIG_RAW_VOLUME"] <= 120]
e3 = e3[e3["ORIG_RAW_VOLUME"] <= 350]

# 3️⃣ Convertir EFFECTIVE_DATE a formato de fecha
e1["EFFECTIVE_DATE"] = pd.to_datetime(e1["EFFECTIVE_DATE"], errors='coerce')
e2["EFFECTIVE_DATE"] = pd.to_datetime(e2["EFFECTIVE_DATE"], errors='coerce')
e3["EFFECTIVE_DATE"] = pd.to_datetime(e3["EFFECTIVE_DATE"], errors='coerce')

# Agregar columna de empresa e identificarla con One-Hot Encoding
e1["empresa"] = "EICH101"
e2["empresa"] = "EICH102"
e3["empresa"] = "EICH104"

# Unificar los tres DataFrames en uno solo
df = pd.concat([e1, e2, e3], ignore_index=True)

# Aplicar One-Hot Encoding a la columna "empresa"
df = pd.get_dummies(df, columns=["empresa"])

# 4️⃣ Eliminar registros con valores nulos, duplicados y negativos
df = df.dropna()  # Eliminar registros con valores nulos
df = df.drop_duplicates()  # Eliminar duplicados
# Seleccionar solo columnas numéricas antes de eliminar valores negativos
numeric_columns = df.select_dtypes(include=["number"]).columns
df = df[df[numeric_columns].ge(0).all(axis=1)]


# 5️⃣ Aplicar normalización Z-score
scaler = StandardScaler()
columns_to_normalize = ["STD_VOLUME", "ORIG_STD_VOLUME", "ORIG_TEMPERATURE","TEMPERATURE","PRESSURE","ORIG_PRESSURE","RAW_VOLUME","ORIG_RAW_VOLUME"]  # Ajusta si necesitas más
df[columns_to_normalize] = scaler.fit_transform(df[columns_to_normalize])

# 6️⃣ Guardar el resultado en un CSV en la misma carpeta donde está el pipeline
output_path = "datos_procesados.csv"
df.to_csv(output_path, index=False)

print(f"Archivo guardado en {output_path}")
