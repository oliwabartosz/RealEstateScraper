from ai_python.columns import FLATS_COLS, FLATS_COLS_TO_GET, HOUSES_COLS_TO_GET, HOUSES_COLS
from ai_python.utils import merge_dicts_by_key
from src.handlers import api_handler
from src.handlers.api_handler import get_offers_data_from_api
import pandas as pd

offer_type = str(input("F, H, P?: "))

# match statement starts here .
match offer_type:
    case "F":
        path = '/rer/api/flats/'
        columns_to_get = FLATS_COLS_TO_GET
        offers_dict = FLATS_COLS
    case "H":
        path = '/rer/api/houses/'
        columns_to_get = HOUSES_COLS_TO_GET
        offers_dict = HOUSES_COLS
    case "P":
        path = '/rer/api/plots/'
        columns_to_get = PLOTS_COLS_TO_GET
        offers_dict = PLOTS_COLS
    case _:
        path = ''
        columns_to_get = []
        offers_dict = {}
        raise Exception('Wrong answer. Must by F, H or P!')

jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')
data = get_offers_data_from_api(jwt_data['access_token'], path, 'GET', '')

expected_dict = {value: '' for value in offers_dict.values()}
expected_dict['status'] = 'new'
input_to_df = []

for record in data:
    merged_dict = merge_dicts_by_key(expected_dict, record)
    input_to_df.append(merged_dict)

df = pd.DataFrame(input_to_df).drop_duplicates().to_csv('output.csv', index=False, header=False)
