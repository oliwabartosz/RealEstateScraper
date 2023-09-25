import json

from langchain.chains import SequentialChain

from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain

# Translator
import translators as ts
import requests
from contextlib import suppress


def test_gpt(chain: list, output_vars: list[str], input_data_json: str):
    # Load data

    with open(f'./src/gpt/test/test-data/{input_data_json}', mode='r', encoding='utf-8') as file:
        data = json.load(file)

    for offer_record in data[1:2]:
        offer_description = offer_record['description']

        offer_description_en = ts.translate_text(offer_description, translator='baidu', to_language='en')

        overall_chain = SequentialChain(
            chains=chain,
            input_variables=['real_estate_offer_en'],
            output_variables=output_vars,
            verbose=True,
        )

        overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en})
        print(overall_chain_result)
