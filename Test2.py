import pandas as pd

df = pd.read_excel(r"D:\Doc\OneDrive\Nokia\Archivo Carga.xlsx")

# Mostrar nombres de columnas
print("Columnas en el DataFrame:")
print(df.columns.tolist())

# Mostrar los primeros valores de cada columna
print("\nPrimeros valores por columna:")
for col in df.columns:
    print(f"{col}: {df[col].head(3).tolist()}")
