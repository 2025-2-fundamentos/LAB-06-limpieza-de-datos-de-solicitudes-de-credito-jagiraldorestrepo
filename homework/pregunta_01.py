"""
Escriba el codigo que ejecute la accion solicitada en la pregunta.
"""


def pregunta_01():
    """
    Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
    El archivo tiene problemas como registros duplicados y datos faltantes.
    Tenga en cuenta todas las verificaciones discutidas en clase para
    realizar la limpieza de los datos.

    El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"

    """

import os as sistema_operativo
import pandas as pandas_lib


def estandarizar_texto(
    columna: pandas_lib.Series, quitar_espacios: bool = True
) -> pandas_lib.Series:
    texto_estandarizado = columna.str.lower().str.replace(r"[ .-]", "_", regex=True)
    return texto_estandarizado.str.strip() if quitar_espacios else texto_estandarizado


def procesar_dataframe(tabla: pandas_lib.DataFrame) -> pandas_lib.DataFrame:
    tabla = tabla.dropna().copy()

    tabla["monto_del_credito"] = (
        tabla["monto_del_credito"]
        .str.replace("$ ", "", regex=False)
        .str.replace(",", "")
        .astype(float)
    )

    columnas_categoricas = [
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "línea_credito",
    ]
    for columna_cat in columnas_categoricas:
        tabla[columna_cat] = estandarizar_texto(
            tabla[columna_cat], quitar_espacios=(columna_cat != "barrio")
        ).astype("category")

    tabla["sexo"] = tabla["sexo"].str.lower().astype("category")
    tabla["estrato"] = tabla["estrato"].astype("category")
    tabla["comuna_ciudadano"] = tabla["comuna_ciudadano"].astype(int).astype("category")
    tabla["fecha_de_beneficio"] = pandas_lib.to_datetime(
        tabla["fecha_de_beneficio"], dayfirst=True, format="mixed"
    )

    tabla.drop_duplicates(inplace=True)
    return tabla


def pregunta_01():
    df = pandas_lib.read_csv(
        "files/input/solicitudes_de_credito.csv", sep=";", index_col=0
    )
    df = procesar_dataframe(df)
    sistema_operativo.makedirs("files/output", exist_ok=True)
    df.to_csv("files/output/solicitudes_de_credito.csv", sep=";")