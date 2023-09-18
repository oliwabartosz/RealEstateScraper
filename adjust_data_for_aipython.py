from src.handlers import api_handler
from src.handlers.api_handler import get_offers_data_from_api
import pandas as pd


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


FLATS_COLS = {
    "Numer oferty": "offerId",
    "Numer oferty pożądany": "offerIdExpected",
    "Typ oferty": "offerType",
    "Status": "offerStatus",
    "Data dodania": "dateAdded",
    "Data zmiany": "dateChanged",
    "Data aktualizacji": "dateUpdated",
    "Data zamknięcia transakcji": "dateEndTransaction",
    "Lokalizacja": "localization",
    "Ulica": "street",
    "Stan prawny": "lawStatus",
    "SWO ID": "skipOffer",
    "Cena": "price",
    "Cena ofertowa": "priceOffer",
    "Cena transakcyjna": "priceSold",
    "Powierzchnia": "livingArea",
    "Balkon": "balcony",
    "Rynek": "market",
    "Cena za m2": "priceM2",
    "Czynsz administracyjny": "rent",
    "Materiał": "material",
    "Stan mieszkania": "flatQuality",
    "Cena z miejscami parkingowymi": "price_with_parking",
    "Cena z wszelkimi dodatkami": "price_with_addings",
    "Piętro": "floor",
    "Ogród": "garden",
    "Liczba pięter": "floorsNumber",
    "Winda": "elevator",
    "Garaż/Miejsca parkingowe": "parkingPlace",
    "Rodzaj budynku": "buildingType",
    "Rok budowy": "yearBuilt",
    "Stan budynku": "buildingQuality",
    "Ochrona": "security",
    "Teren strzeżony": "guardedArea",
    "Monitoring": "monitoring",
    "Kontrola dostępu": "securityControl",
    "Liczba pokoi": "roomsNumber",
    "Typ kuchni": "kitchenType",
    "Piwnica": "basement",
    "Liczba balkonów": "balconyQuantity",
    "Opis": "description",
    "Uwagi": "comments",
    "Osiedle strzeżone": "guardedEstate",
    "Recepcja": "reception",
    "Liczba loggi": "loggiasQuantity",
    "Komórka": "storageRoom",
    "Poddasze użytkowe": "attic",
    "Liczba tarasów": "terracesQuantity",
    "Liczba balkonów francuskich": "frenchBalconyQuantity",
    "Numer zewnętrzny": "outside_no",
    "Cena za parking podziemny (miejsce)": "priceParkingUnderground",
    "Cena za parking naziemny (miejsce)": "priceParkingGround",
    "Uwagi dla użytkowników z SWO/MLS": "swo_comment",
    "balkon": "balconyDesc",
    "francu": "frenchBalconyDesc",
    "taras": "terraceDesc",
    "wind": "elevatorDesc",
    "piwnic": "basementDesc",
    "komórk": "storageroomDesc",
    "strych": "atticDesc",
    "gospodarcze": "utilityroomDesc",
    "postojow": "parkingSpaceDesc",
    "parking": "parkingPlaceDesc",
    "przynależn": "belongingDesc",
    "garaż": "garageDesc",
    "możliwość": "possibilityDesc",
    "ogród": "gardenDesc",
    "ogrod": "gardenDesc2",
    "działka": "gardenDesc3",
    "ocieplony": "insulatedBuildingDesc",
    "moderniz": "modernizatedBuildingDesc",
    "odrestaur": "restoredBuildingDesc",
    "odnow": "renewedBuildingDesc",
    "ociepl": "insulatedBuildingDesc2",
    "remon": "renovationDesc",
    "elewac": "elevationDesc",
    "dozór": "supervisionDesc",
    "dozor": "supervisionDesc2",
    "monitoring": "monitoringDesc",
    "monit": "monitoringDesc2",
    "ochron": "securityDesc",
    "alarm": "alarmDesc",
    "strzeż": "guardedDesc",
    "portier": "doorkeeperDesc",
    "wspólnot": "communityFlatDesc",
    "spółdziel": "cooperativeflatDesc",
    "kuchni": "kitchenDesc",
    "aneks": "kitchenAnnexDesc",
    "widna": "kitchenBrightDesc",
    "ciemna": "kitchenDarkDesc",
    "prześwit": "kitchenClearanceDesc",
    "z oknem": "kitchenWindowDesc",
    "z jadalni": "kitchenDiningRoomDesc",
    "oficyn": "outbuildingDesc",
    "linia": "outbuildingDesc2",
    "linii": "outbuildingDesc3",
    "opłat": "feesDesc",
    "bezczynsz": "withoutRentDesc",
    "czynsz": "rentDesc",
    "poziom": "levelDesc",
    "ul.": "ul1",
    "al.": "al1",
    " zł": "zl1",
    " zl": "zl2",
    "pln": "zl3",
    "ul\.": "ul2",
    "al\.": "al2",
    "status": "new",
}

expected_dict = {value: '' for value in FLATS_COLS.values()}
expected_dict['status'] = 'new'

jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')
data = get_offers_data_from_api(jwt_data['access_token'], '/rer/api/flats/', 'GET',
                                'offerId', 'offerIdExpected', 'offerType', 'offerStatus', 'dateAdded', 'dateChanged',
                                'dateUpdated',
                                'dateEndTransaction', 'localization', 'street', 'lawStatus', 'price',
                                'priceOffer', 'priceSold',
                                'livingArea', 'balcony', 'market', 'priceM2', 'rent', 'material', 'flatQuality',
                                'floor', 'garden', 'floorsNumber', 'elevator', 'parkingPlace', 'buildingType',
                                'yearBuilt', 'buildingQuality', 'security', 'guardedArea',
                                'monitoring', 'securityControl', 'roomsNumber', 'kitchenType', 'basement',
                                'balconyQuantity', 'description', 'balconyQuantity', 'description', 'guardedEstate',
                                'loggiasQuantity', 'storageRoom', 'attic', 'terracesQuantity', 'frenchBalconyQuantity',
                                'priceParkingUnderground', 'priceParkingGround',
                                'balconyDesc', 'frenchBalconyDesc', 'terraceDesc', 'elevatorDesc', 'basementDesc',
                                'storageroomDesc', 'atticDesc', 'utilityroomDesc', 'parkingSpaceDesc',
                                'parkingPlaceDesc', 'belongingDesc', 'garageDesc', 'possibilityDesc',
                                'gardenDesc', 'gardenDesc2', 'gardenDesc3', 'insulatedBuildingDesc',
                                'modernizatedBuildingDesc', 'restoredBuildingDesc', 'renewedBuildingDesc',
                                'insulatedBuildingDesc2', 'renovationDesc', 'elevationDesc', 'supervisionDesc',
                                'supervisionDesc2', 'monitoringDesc', 'monitoringDesc2', 'securityDesc', 'alarmDesc',
                                'guardedDesc', 'doorkeeperDesc', 'communityFlatDesc', 'cooperativeflatDesc',
                                'kitchenDesc', 'kitchenAnnexDesc', 'kitchenBrightDesc', 'kitchenDarkDesc',
                                'kitchenClearanceDesc', 'kitchenWindowDesc', 'kitchenDiningRoomDesc', 'outbuildingDesc',
                                'outbuildingDesc2', 'outbuildingDesc3', 'feesDesc', 'withoutRentDesc', 'rentDesc',
                                'levelDesc'
                                )

input_to_df = []

for record in data:
    merged_dict = merge_dicts_by_key(expected_dict, record)
    input_to_df.append(merged_dict)

df = pd.DataFrame(input_to_df).drop_duplicates().to_csv('output.csv', index=False, header=False)

# Dodaj "pominięte kolumny"
# Dodaj warunki dla NULLi
# Co ze 'status'?
