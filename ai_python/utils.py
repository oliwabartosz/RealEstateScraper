def add_data_after_key(original_dict, specific_key, new_key, new_value=''):
    new_dict = {}

    for key, value in original_dict.items():
        new_dict[key] = value  # Copy all key-value pairs from the original dictionary

        if key == specific_key:
            new_dict[new_key] = new_value  # Add the new key-value pair after the specific key

    return new_dict


def merge_dicts_by_key(dict1, dict2):
    merged_dict = dict1.copy()
    for key, value in dict2.items():
        if key in merged_dict:
            merged_dict[key] = value
    return merged_dict
