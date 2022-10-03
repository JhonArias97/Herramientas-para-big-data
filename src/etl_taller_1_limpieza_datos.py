# importar librerias de manipulacion de datos
import numpy as np 
import pandas as pd
from dateutil.parser import parse
from pkgutil import get_data

# importar librerias del sistema
import os
from pathlib import Path

def main():

    # Leer archivo
    data = get_data(filename = "llamadas123_julio_2022.csv")
    # Extraer resumen
    df_clean = get_clean(data = data)
    # Guardar el resumen
    save = save_data(df_clean)

def get_data(filename):

    root_dir = Path(".").resolve()
    data_dir = "raw"
    file_path = os.path.join(root_dir, "data", data_dir, filename)
    data = pd.read_csv(file_path, encoding= "latin-1", sep = ";")
    return(data)

def get_clean(data):

    #Primero hacemos la limpieza de los duplicados
    data = data.drop_duplicates()


    # Sobreeescribo la columna UNIDAD que tenia valores nulos por una columna sin nulos
    data["UNIDAD"] = data["UNIDAD"].fillna("SIN_DATO")


    # Convertir columna en formato fecha
    col = "FECHA_INICIO_DESPLAZAMIENTO_MOVIL"
    data[col] = pd.to_datetime(data[col], errors = "coerce")


    #Reiniciamos el indiced e nuestra tabla y creo una funcion que me permitira convertir los formatos a fechas
    data = data.reset_index()

    def convertir_formato_fecha(str_fecha):
        val_datetime = parse(str_fecha, dayfirst = True)
        return val_datetime


    # Ejecuto un ciclo que me permita hacer el cambio de fechas y crearlo en una nueva lista
    list_fechas = list()
    n_filas = data.shape[0]

    for i in range(0, n_filas):
        
        str_fecha = data["RECEPCION"][i]

        try:
            val_datetime = convertir_formato_fecha(str_fecha= str_fecha)
            list_fechas.append(val_datetime)
        except Exception as e:
            list_fechas.append(str_fecha)
            continue

    data["RECEPCION_CORREGIDA"] = list_fechas

    # Convierto la columna creada a formato fecha y luego reemplazo la columna original
    data["RECEPCION_CORREGIDA"] = pd.to_datetime(data["RECEPCION_CORREGIDA"], errors = "coerce")

    data["RECEPCION"] = data["RECEPCION_CORREGIDA"]

    #Elimino la columna creada de correcion
    data = data.drop(["RECEPCION_CORREGIDA"], axis=1)

    #Reemplazamos los sin datos por valores nulos, para poder convertir la columna a tipo numerico
    data["EDAD"] = data["EDAD"].replace({"SIN_DATO": np.nan})

    #Convertimos la columna a tipo numerico
    data["EDAD"] = pd.to_numeric(data["EDAD"], errors = "coerce")

    #Reemplazo los valores que tienen caracteres especiales con su respectivo nombre
    data['LOCALIDAD']= data['LOCALIDAD'].replace(['Fontib¢n','Engativ ',"Ciudad Bol¡var","Usaqun","San Crist¢bal","Los M rtires", "Antonio Nari¤o"],
                                                ['Fontibon','Engativa',"Ciudad Bolivar","Usaquen","San Cristobal", "Los Martires","Antonio Narino"])

    #Reemplazo los valores que tienen caracteres especiales con su respectivo nombre
    data['UNIDAD']= data['UNIDAD'].replace(["A¤os"],
                                        ["Anos"])

    return(data)

def save_data(df_clean):

    root_dir = Path(".").resolve()
    filename = "llamadas123_julio_2022.csv"
    out_name = "Taller_1_Datos_limpios_" + filename
    out_path = os.path.join(root_dir, "data", "processed", out_name)
    df_clean.to_csv(out_path)    


if __name__ == '__main__':
    main()