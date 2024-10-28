import pandas as pd
import geopandas as gpd

def load_data():
    url = 'https://dados.agricultura.gov.br/dataset/baefdc68-9bad-4204-83e8-f2888b79ab48/resource/ac7e4351-974f-4958-9294-627c5cbf289a/download/psrdadosabertos2024csv.csv'
    # Carregar os dados de seguros diretamente de uma URL e definir o encoding e separador
    df = pd.read_csv(url, encoding='latin1', sep=';', low_memory=False)
    return df

# Carregar os dados de seguros usando a função cacheada
df = load_data()

df.drop(columns=['CD_PROCESSO_SUSEP', 'NR_PROPOSTA', 'ID_PROPOSTA',
                 'DT_PROPOSTA', 'DT_INICIO_VIGENCIA', 'DT_FIM_VIGENCIA', 'NM_SEGURADO',
                 'NR_DOCUMENTO_SEGURADO', 'LATITUDE', 'NR_GRAU_LAT', 'NR_MIN_LAT',
                 'NR_SEG_LAT', 'LONGITUDE', 'NR_GRAU_LONG', 'NR_MIN_LONG', 'NR_SEG_LONG',
                 'NR_DECIMAL_LATITUDE', 'NR_DECIMAL_LONGITUDE',
       'NivelDeCobertura','DT_APOLICE',
       'ANO_APOLICE', 'CD_GEOCMU'], inplace=True)

df.to_parquet('assets/dados_filtrados.parquet')


def load_geodata():
    # Carregar o shapefile com os estados do Brasil
    return gpd.read_file('datasets/BR_UF_2022.shp')


# Carregar os dados geográficos usando a função cacheada
gdf = load_geodata()

# Define a tolerância para a simplificação (ajuste o valor conforme necessário)
tolerancia = 0.01  # Unidade é geralmente em graus, ajuste conforme a precisão desejada

# Aplica a simplificação mantendo a topologia
gdf['geometry'] = gdf['geometry'].simplify(tolerance=tolerancia, preserve_topology=True)

# Remove colunas desnecessárias
gdf.drop(columns=['CD_UF', 'NM_UF', 'NM_REGIAO', 'AREA_KM2'], inplace=True)

# Salva o GeoDataFrame simplificado em GeoJSON
gdf.to_file('assets/BR_UF_2022_filtrado.geojson', driver='GeoJSON')