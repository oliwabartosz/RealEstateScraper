def handle_law_status_param(offer_params: dict) -> int:
    law_status = offer_params.get('lawStatus', -9)

    if law_status == 'Własność':
        return 1
    elif "Spółdzielcze własnościowe" in law_status:
        return 2
    else:
        return law_status


def handle_elevator_param(offer_params: dict) -> int:
    floors_number: bool = int(offer_params.get('floorsNumber', 0)) > 5

    if floors_number or offer_params.get('elevator') == 'Tak':
        return 1
    elif not floors_number or offer_params.get('elevator') == 'Nie':
        return 0
    else:
        return -9


def handle_kitchen_param(offer_params: dict) -> int:
    kitchen_param = offer_params.get('kitchenType', -9)

    if kitchen_param == 'Ciemna' or 'Prześwit' or 'Inny':
        return 1
    elif kitchen_param == "Widna":
        return 2
    elif kitchen_param == "Aneks":
        return 3
    else:
        return int(kitchen_param)


def handle_balcony_param(offer_params: dict) -> int:
    balcony_param = offer_params.get('balcony', -9)
    french_balcony_quantity = int(offer_params.get('frenchBalconyQuantity', -9))

    if balcony_param == 'Tak' and french_balcony_quantity > 0:
        return 0
    elif balcony_param == 'Tak' and french_balcony_quantity < 0:
        return 1
    elif balcony_param == 'Nie':
        return 0
    else:
        return balcony_param


def handle_monitoring_param(offer_params: dict) -> int:
    monitoring_params = ['monitoring', 'guardedArea', 'guardedEstate', 'security', 'securityControl']
    for param in monitoring_params:
        if offer_params.get(param) == 'Tak':
            return 1

    return -9


def handle_basement_param(offer_params: dict) -> int:
    basement_param = offer_params.get('balcony', -9)

    if basement_param == 'Tak':
        return 1
    elif basement_param == 'Nie':
        return 0

    return -9


def handle_garage_param(offer_params: dict) -> int:
    parking_under_price_param = offer_params.get('priceParkingUnderground', -9)
    parking_ground_price_param = offer_params.get('priceParkingGround', -9)

    if any(int(float(parking_price)) > 0 for parking_price in [parking_under_price_param, parking_ground_price_param]):
        return 0
    return -9


def handle_garden_param(offer_params: dict) -> int:
    return 1 if offer_params.get('garden', -9) == 'Tak' else 0 if offer_params.get('garden', -9) == 'Nie' else -9


def handle_outbuilding_param(offer_params: dict) -> int:
    return 1 if offer_params.get('buildingType', -9) == 'Oficyna' else -9


def handle_rent_param(offer_params: dict) -> int:
    return int(float(offer_params.get('rent', -9)))
