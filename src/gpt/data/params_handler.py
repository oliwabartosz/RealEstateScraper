def handle_law_status_param(offer_params: dict) -> int:
    law_status = offer_params.get('lawStatus', -9)

    if law_status == 'Własność':
        return 1
    elif "Spółdzielcze własnościowe" in law_status:
        return 2
    else:
        return law_status


def handle_rent_param(offer_params: dict) -> int:
    return offer_params.get('rent', -9)
    # return -9 if not isinstance(rent_param, (int, float)) else rent_param
    # rent_param = offer_params.get('rent', '')
    # return -9 if not isinstance(rent_param, (int, float)) else rent_param


def handle_elevator_param(offer_params: dict) -> int:
    floors_number: bool = int(offer_params.get('floorsNumber', 0)) > 5

    if floors_number or offer_params.get('elevator') == 'Tak':
        return 1
    elif not floors_number or offer_params.get('elevator') == 'Nie':
        return 0
    else:
        return -9





def handle_kitchen_param(offer_params: dict) -> int:
    kitchen_param = offer_params.get('kitchenType', '')

    if kitchen_param == 'Ciemna' or 'Prześwit' or 'Inny':
        return 1
    elif kitchen_param == "Widna":
        return 2
    elif kitchen_param == "Aneks":
        return 3
    else:
        return int(kitchen_param)
