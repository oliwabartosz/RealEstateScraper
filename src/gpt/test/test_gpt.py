import json
import re
from typing import TypeVar

DataFrame = TypeVar('DataFrame')

import pandas

# pandas.set_option('display.max_colwidth', None)
pandas.set_option('display.max_columns', None)

# Translator
import translators as ts
from langchain.chains import SequentialChain


def test_gpt(chain: list, output_vars: list[str], parameters: bool, input_data_json: str, verbose=False) -> tuple[
    float, DataFrame]:
    rating_pattern = '_rating$'
    summary_pattern = '_summary$'

    if not (bool(re.search(rating_pattern, output_vars[1])) and bool(re.search(summary_pattern, output_vars[0]))):
        raise ValueError(f'output_vars error. The first value should have _summary in name, the second one should have'
                         f'_rating, ie. ["balcony_summary", "balcony_rating"]. You have got {output_vars}.')

    # Load data
    with open(f'./src/gpt/test/test-data/{input_data_json}', mode='r', encoding='utf-8') as file:
        data = json.load(file)

    results = []
    for i, offer_record in enumerate(data):
        offer_description = offer_record['description']

        offer_description_en = ts.translate_text(offer_description, translator='baidu', to_language='en')
        if parameters:
            offer_parameters_pl = {key: value for key, value in offer_record.items() if
                                   key not in ['id', 'number', 'description', 'desiredOutput']}
            offer_parameters_en = ts.translate_text(str(offer_parameters_pl), translator='bing', to_language='en')

        print(f'{i + 1}/{len(data)}: LLM Chaining..')

        input_variables = ['real_estate_offer_en']
        if parameters: input_variables.append('offer_parameters_en')

        overall_chain = SequentialChain(
            chains=chain,
            input_variables=input_variables,
            output_variables=output_vars,
            verbose=False,
        )

        if parameters:
            overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en,
                                                  "offer_parameters_en": offer_parameters_en})
        else:
            overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en})

        print(f"""id: {offer_record['id']}, 
        LLM Rating: {overall_chain_result[output_vars[1]]}, 
        Desired Rating: {offer_record['desiredOutput']}
        {('Parameters: ' + offer_parameters_en if verbose else '') if parameters else ''}
        LLM Summary: {overall_chain_result[output_vars[0]]}
        Description: {offer_description_en}
        """)

        result = {
            'id': offer_record['id'],
            'rating': overall_chain_result[output_vars[1]],
            'rating_summary': overall_chain_result[output_vars[0]],
            'desired_output': offer_record['desiredOutput'],
            'description': offer_description_en,
            'descriptionPL': offer_description
        }

        results.append(result)

    df = pandas.DataFrame(results)

    df['rating'] = pandas.to_numeric(df['rating'])
    df['desired_output'] = pandas.to_numeric(df['desired_output'], errors='coerce')

    success_rate = df['rating'].eq(df['desired_output']).mean()

    # Calculate the mismatched rows
    mismatched_rows = df[df['rating'] != df['desired_output']]
    mismatched_rows.index = mismatched_rows.index + 1

    # Save to JSON.
    output_name_base = input_data_json.strip('.json')

    df.to_json(f'./src/gpt/test/test-data/output/{output_name_base}.json', orient="records")
    mismatched_rows.to_json(f'./src/gpt/test/test-data/output/{output_name_base}_mismatch.json', orient="records",
                            index=True, force_ascii=False)

    if verbose:
        # Print success rate
        print('Success rate is:', success_rate)

        # Print the mismatched rows
        print('Mismatch: \n', mismatched_rows)

    return success_rate, mismatched_rows
