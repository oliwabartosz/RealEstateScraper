def handle_law_status_param(offer_params: dict) -> int:
    law_status = offer_params.get('lawStatus', '')

    if law_status == 'Własność':
        law_param = 1
    elif "Spółdzielcze własnościowe" in law_status:
        law_param = 2
    else:
        law_param = law_status

    return law_param


def handle_rent_param(offer_params: dict) -> int:
    rent_param = offer_params.get('rent', '')
    return -9 if not isinstance(rent_param, (int, float)) else rent_param


def handle_elevator_param(offer_params: dict) -> int:
    return int(offer_params.get('floorsNumber', 0)) > 5 and offer_params.get('elevator') == 'Tak'


def handle_kitchen_param(offer_params: dict) -> int:
    kitchen_param = offer_params.get('kitchenType', '')

    if kitchen_param == 'Ciemna' or 'Prześwit' or 'Inny':
        kitchen_param = 1
    elif kitchen_param == "Widna":
        kitchen_param = 2
    elif kitchen_param == "Aneks":
        kitchen_param = 3
    else:
        kitchen_param = kitchen_param

    return kitchen_param
