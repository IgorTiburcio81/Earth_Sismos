from datetime import datetime, timedelta
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

USGS_URL = os.getenv('USGS_BASE_URL')

def janela_temp (data_inicial_str, data_final_str, dia_janelas=90):

    data_atual = datetime.strptime(data_inicial_str, "%Y-%m-%d")
    data_final = datetime.strptime(data_final_str, "%Y-%m-%d")

    janelas = []

    while data_atual < data_final:

        proxima_data = data_atual + timedelta(days=dia_janelas)
        if proxima_data > data_final:
            proxima_data = data_final
        janelas.append( (data_atual.strftime("%Y-%m-%d"), proxima_data.strftime("%Y-%m-%d")) ) 
        data_atual = proxima_data + timedelta(days=1)           
    return janelas

def requ_retry (url, params, max_tent=3):
    for tent in range(max_tent):
        try:
            resp = requests.get(url, params=params, timeout=30)

            if resp.status_code == 200
                return resp.json()
            print(f"Tentativa {tent + 1} falhou. Status code: {resp.status_code}")
        except Exception as e:
            print(f"Tentativa {tent + 1} falhou por erro de conexão: {e}")

        if tent < max_tent -1:
            print(f"Aguardando 5 segundos antes da tentativa {tent + 2}...")
            time.sleep(5)
    raise Exception(f"Falha total ao buscar dados na API após {max_tent} tentativas.")
