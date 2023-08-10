
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
