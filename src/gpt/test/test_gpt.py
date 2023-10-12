from src.gpt.gpt import start_gpt_assessment
import json
import re

# Typing
from typing import TypeVar

DataFrame = TypeVar('DataFrame')

# DataFrames
import pandas

pandas.set_option('display.max_columns', None)

# Config data
from src.config import config_data
from operator import itemgetter

data = config_data.get_config_data()
translator = itemgetter('translator')(data)


def test_gpt(param: str, input_data_json: str) -> list[dict]:
    params = [param]
    results = []

    if not params:
        raise ValueError("params can't be empty")

    with open(f'./src/gpt/test/test-data/{input_data_json}', mode='r', encoding='utf-8') as file:
        data_json = json.load(file)

    for record in data_json:
        print(record)
        assessment = start_gpt_assessment(start=0, end=None, retry=False, data=[record], offers_type='flats',
                                          api=False,
                                          take_result_from_offer_params=False, include_params=params)
        assessment['desiredOutput'] = record['desiredOutput']
        del assessment['qualityGPT']
        del assessment['status']
        results.append(assessment)

    return results


def insert_results_to_df(results: list[dict], verbose: bool, input_data_json: str) -> tuple[float, DataFrame] | None:
    # Change keys in dicts for rating and summary
    rating_pattern = 'GPT$'
    summary_pattern = '_summary$'

    for d in results:
        for k in list(d.keys()):
            if re.search(rating_pattern, k):
                d['rating'] = d.pop(k)
            if re.search(summary_pattern, k):
                d['GPT_summary'] = d.pop(k)

    # Create DataFrame
    df = pandas.DataFrame(results)
    print(df)

    df['rating'] = pandas.to_numeric(df['rating'])
    df['desired_output'] = pandas.to_numeric(df['desiredOutput'], errors='coerce')

    success_rate = df['rating'].eq(df['desired_output']).mean()

    if success_rate != 1.0:
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
    else:
        print('Success rate is:', success_rate)


def start_test(parameter: str) -> None:
    """
    Starts test for specified parameter.
    :param parameter: choose one of the following: 'balcony', 'basement', 'elevator', 'garage', 'garden', 'kitchen',
    'lawStatus', 'modernization', 'monitoring', 'outbuilding', 'technology'
    :return: None. Creates json output in output folder and prints success rate.
    """
    if parameter not in ['balcony', 'basement', 'elevator', 'garage', 'garden', 'kitchen',
                         'lawStatus', 'modernization', 'monitoring', 'outbuilding', 'technology']:
        raise ValueError('Wrong parameter name.')

    test = test_gpt(parameter, f'test-{parameter}.json')
    insert_results_to_df(test, True, f'test-{parameter}.json')
