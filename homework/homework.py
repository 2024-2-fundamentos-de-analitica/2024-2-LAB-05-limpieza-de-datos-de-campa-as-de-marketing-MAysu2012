"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import os
import pandas as pd
from zipfile import ZipFile

def procesar_datos_campaña():
    """
    Limpia y transforma los datos de una campaña de marketing de un banco, 
    separando la información en tres archivos CSV: clientes.csv, campaña.csv 
    y economía.csv, después de procesar los archivos CSV comprimidos en zip.
    """

    mapa_meses = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", 
        "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", 
        "nov": "11", "dec": "12"
    }

    directorio_entrada = os.path.join("files", "input")
    directorio_salida = os.path.join("files", "output")
    
    os.makedirs(directorio_salida, exist_ok=True)
    
    archivos_zip = [os.path.join(directorio_entrada, f) for f in os.listdir(directorio_entrada)]
    df_combinado = pd.concat([pd.read_csv(ZipFile(archivo_zip).open(ZipFile(archivo_zip).namelist()[0])) for archivo_zip in archivos_zip], ignore_index=True)
    
    df_clientes = df_combinado[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    df_clientes["job"] = df_clientes["job"].str.replace(".", "").str.replace("-", "_")
    df_clientes["education"] = df_clientes["education"].replace("unknown", pd.NA).apply(lambda x: x.replace("-", "_").replace(".", "_") if pd.notna(x) else x)
    df_clientes["credit_default"] = df_clientes["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    df_clientes["mortgage"] = df_clientes["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    # Filtrando y procesando 
    df_campaña = df_combinado[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "month", "day"]].copy()
    df_campaña["month"] = df_campaña["month"].apply(lambda x: mapa_meses.get(x.lower(), "00"))
    df_campaña["previous_outcome"] = df_campaña["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    df_campaña["campaign_outcome"] = df_campaña["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    df_campaña["month"] = df_campaña["month"].astype(str).str.zfill(2)
    df_campaña["day"] = df_campaña["day"].astype(str).str.zfill(2)
    df_campaña["last_contact_date"] = "2022-" + df_campaña["month"] + "-" + df_campaña["day"]
    df_campaña.drop(columns=["month", "day"], inplace=True)

    
    df_economia = df_combinado[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    # Guardar los DataFrames 
    df_clientes.to_csv(os.path.join(directorio_salida, "clientes.csv"), index=False)
    df_campaña.to_csv(os.path.join(directorio_salida, "campaña.csv"), index=False)
    df_economia.to_csv(os.path.join(directorio_salida, "economía.csv"), index=False)

if __name__ == "__main__":
    procesar_datos_campaña()
    
    
   
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

   # return


#if __name__ == "__main__":
 #   clean_campaign_data()
