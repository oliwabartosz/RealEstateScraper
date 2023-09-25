import json

from langchain.chains import SequentialChain

from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain

# Translator
import translators as ts
import requests
from contextlib import suppress

def test_balcony_gpt():
    balcony_chain = [
        balcony_summary_chain, balcony_rating_chain,
    ]

    balcony_output_variables = [
        "balcony_summary", "balcony_rating",
    ]

    # Load data
    with open('./src/gpt/data/test-data/test-balcony.json', mode='r', encoding='utf-8') as file:
        balcony_data = json.load(file)

    for offer_record in balcony_data[1:2]:
        offer_description = offer_record['description']

        offer_description_en = ts.translate_text(offer_description, translator='baidu', to_language='en')

        overall_chain = SequentialChain(
            chains=balcony_chain,
            input_variables=['real_estate_offer_en'],
            output_variables=balcony_output_variables,
            verbose=True,
        )

        overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en})
        print(overall_chain_result)
