from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain, law_status_summary_chain, \
    law_status_rating_chain, year_of_constr_chain, material_chain, building_type_chain, number_floors_chain, \
    technology_summary_chain, technology_rating_chain, monitoring_summary_chain, monitoring_rating_chain, \
    basement_summary_chain, basement_rating_chain, elevator_rating_chain, elevator_summary_chain, garage_summary_chain, \
    garage_rating_chain, garden_summary_chain, garden_rating_chain, kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain, outbuilding_summary_chain, outbuilding_rating_chain
from src.gpt.test.test_gpt import test_gpt


def start_balcony_gpt_test(start=True):
    if start:
        print('Test: balcony:')
        test_gpt([balcony_summary_chain, balcony_rating_chain],
                 ["balcony_summary", "balcony_rating"],
                 False,
                 'test-balcony.json',
                 True
                 )


def start_law_status_test(start=True):
    if start:
        print('Test: lawStatus:')
        test_gpt([law_status_summary_chain, law_status_rating_chain],
                 ["law_summary", "law_rating"],
                 True,
                 'test-law-status.json',
                 True
                 )


def start_technology_test(start=True):
    if start:
        print('Test: technology:')
        test_gpt(
            [year_of_constr_chain, material_chain, building_type_chain, number_floors_chain, technology_summary_chain,
             technology_rating_chain],
            ["technology_summary", "technology_rating"],
            True,
            'test-technology.json',
            True
        )


def start_monitoring_test(start=True):
    if start:
        print('Test: monitoring:')
        test_gpt([monitoring_summary_chain, monitoring_rating_chain],
                 ["monitoring_summary", "monitoring_rating"],
                 False,
                 'test-alarm.json',
                 True
                 )


def start_basement_test(start=True):
    if start:
        print('Test: basement:')
        test_gpt([basement_summary_chain, basement_rating_chain],
                 ["basement_summary", "basement_rating"],
                 False,
                 'test-basement.json',
                 True
                 )


def start_elevator_test(start=True):
    if start:
        print('Test: elevator:')
        test_gpt([elevator_summary_chain, elevator_rating_chain],
                 ["elevator_summary", "elevator_rating"],
                 False,
                 'test-elevator.json',
                 True
                 )


def start_garage_test(start=True):
    if start:
        print('Test: garage:')
        test_gpt([garage_summary_chain, garage_rating_chain],
                 ["garage_summary", "garage_rating"],
                 False,
                 'test-garage.json',
                 True
                 )


def start_garden_test(start=True):
    if start:
        print('Test: garden:')
        test_gpt([garden_summary_chain, garden_rating_chain],
                 ["garden_summary", "garden_rating"],
                 False,
                 'test-garden.json',
                 True
                 )


def start_kitchen_test(start=True):
    if start:
        print('Test: kitchen:')
        test_gpt([kitchen_summary_chain, kitchen_rating_chain],
                 ["kitchen_summary", "kitchen_rating"],
                 False,
                 'test-kitchen.json',
                 True
                 )


def start_modernization_test(start=True):
    if start:
        print('Test: modernization:')
        test_gpt([modernization_summary_chain, modernization_rating_chain],
                 ["modernization_summary", "modernization_rating"],
                 False,
                 'test-modernization.json',
                 True
                 )


def start_outbuilding_test(start=True):
    if start:
        print('Test: outbuilding:')
        test_gpt([outbuilding_summary_chain, outbuilding_rating_chain],
                 ["outbuilding_summary", "outbuilding_rating"],
                 False,
                 'test-outbuilding.json',
                 True
                 )
