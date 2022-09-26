# Pseudo codigo
# 1. leer archivo .csv
# 2. estraer el resumen
# 3. guardar el resumen en formato en .csv

from pkgutil import get_data
import numpy as np
import pandas as pd
import os
from pathlib import Path


def main():

    # Leer archivo
    data = get_data(filename = "llamadas123_julio_2022.csv")
    # Extraer resumen
    df_resume = get_summary(data = data)
    # Guardar el resumen
    save = save_data(df_resume)


def get_data(filename):
    data_dir = "raw"
    root_dir = Path(".").resolve()
    file_path = os.path.join(root_dir, "data", data_dir, filename)

    data = pd.read_csv(file_path, encoding = "latin-1", sep = ";")
    #print(data.shape)

    return(data)

def get_summary(data):
    # Crear un diccionario vacio
    dict_resumen = dict()

    for columnas in data.columns:
        valores_unicos = data[columnas].unique()
        n_valores = len(valores_unicos)
        #print(columnas, n_valores)
        dict_resumen[columnas] = n_valores

    df_resumen = pd.DataFrame.from_dict(dict_resumen, orient = "index")
    #df_resumen.rename({0: "count"}, axis = 1, inplace = True)
    return(df_resumen)

def save_data(df_resumen):
    root_dir = Path(".").resolve()
    filename = "llamadas123_julio_2022.csv"
    out_name = "resumen2_" + filename
    out_path = os.path.join(root_dir, "data", "processed", out_name)
    df_resumen.to_csv(out_path)


if __name__ == '__main__':
    main()
