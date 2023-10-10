from operator import itemgetter

import translators as ts

# Import translator setting from config
from src.config import config_data
data = config_data.get_config_data()
translator = itemgetter('translator')(data)


def merge_dictionaries_by_id(list1: list, list2: list) -> list:
    merged_dict = {}

    # Merge dictionaries from list1
    for item in list1:
        item_id = item['id']
        merged_dict.setdefault(item_id, {}).update(item)

    # Merge dictionaries from list2
    for item in list2:
        item_id = item['id']
        merged_dict.setdefault(item_id, {}).update(item)

    # Convert merged_dict back to a list of dictionaries
    merged_list = list(merged_dict.values())

    return merged_list


def translate_result_to_pl(dict_to_translate: dict, language: str, *exclude_keys) -> dict:
    print('Translating the result..')
    translated_dict = {}

    for key, value in dict_to_translate.items():
        if key not in exclude_keys:
            value = ts.translate_text(str(value), translator=translator, to_language=language)
        translated_dict[key] = value

    return translated_dict
