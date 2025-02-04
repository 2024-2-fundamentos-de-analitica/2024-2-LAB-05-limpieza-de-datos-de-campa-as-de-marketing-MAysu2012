"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel
import os
import pandas as pd
from zipfile import ZipFile

def process_campaign_data():
    """
    Limpia y transforma los datos de una campaña de marketing de un banco, 
    separando la información en tres archivos CSV: client.csv, campaign.csv 
    y economics.csv, después de procesar los archivos CSV comprimidos en zip.
    """

    month_map = {
        "jan": "01", "feb": "02", "mar": "03", "apr": "04", "may": "05", 
        "jun": "06", "jul": "07", "aug": "08", "sep": "09", "oct": "10", 
        "nov": "11", "dec": "12"
    }

    input_dir = os.path.join("files", "input")
    output_dir = os.path.join("files", "output")
    
    os.makedirs(output_dir, exist_ok=True)
    
    zip_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir)]
    combined_df = pd.concat([pd.read_csv(ZipFile(zip_file).open(ZipFile(zip_file).namelist()[0])) for zip_file in zip_files], ignore_index=True)
    
    client_df = combined_df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    client_df["job"] = client_df["job"].str.replace(".", "").str.replace("-", "_")
    client_df["education"] = client_df["education"].replace("unknown", pd.NA).apply(lambda x: x.replace("-", "_").replace(".", "_") if pd.notna(x) else x)
    client_df["credit_default"] = client_df["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client_df["mortgage"] = client_df["mortgage"].apply(lambda x: 1 if x == "yes" else 0)

    campaign_df = combined_df[["client_id", "number_contacts", "contact_duration", "previous_campaign_contacts", "previous_outcome", "campaign_outcome", "month", "day"]].copy()
    campaign_df["month"] = campaign_df["month"].apply(lambda x: month_map.get(x.lower(), "00"))
    campaign_df["previous_outcome"] = campaign_df["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign_df["campaign_outcome"] = campaign_df["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    campaign_df["month"] = campaign_df["month"].astype(str).str.zfill(2)
    campaign_df["day"] = campaign_df["day"].astype(str).str.zfill(2)
    campaign_df["last_contact_date"] = "2022-" + campaign_df["month"] + "-" + campaign_df["day"]
    campaign_df.drop(columns=["month", "day"], inplace=True)

    economics_df = combined_df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()

    client_df.to_csv(os.path.join(output_dir, "client.csv"), index=False)
    campaign_df.to_csv(os.path.join(output_dir, "campaign.csv"), index=False)
    economics_df.to_csv(os.path.join(output_dir, "economics.csv"), index=False)

if __name__ == "__main__":
    process_campaign_data()
    
    
   
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
