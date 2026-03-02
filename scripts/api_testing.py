import requests
import pandas as pd

API_URL = "https://plueview-659121705045.europe-west1.run.app/data"
CLIMATE_COLUMNS = ["umidade", "temperatura", "velocidadeVento", "quantidadeChuva"]


def fetch_data(url=API_URL, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None


def get_climate_dataframe(data):
    df = pd.DataFrame(data)
    return df[CLIMATE_COLUMNS]


def validate(climate_df):
    nulos = climate_df.isna().sum()
    if nulos.sum() > 0:
        print("\nProblemas encontrados nos dados da API")
        print("Quantidade de falhas por sensor:")
        print(nulos.to_string())
        return False
    return True


def print_statistics(climate_df):
    stats = climate_df.agg(["mean", "median", "std"])
    print("\n=== Estatísticas Climáticas ===\n")
    print(stats.to_string())


def main():
    data = fetch_data()
    if data is None:
        return

    climate_df = get_climate_dataframe(data)

    if not validate(climate_df):
        return

    print_statistics(climate_df)


if __name__ == "__main__":
    main()  