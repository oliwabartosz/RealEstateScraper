from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain, law_status_summary_chain, \
    law_status_rating_chain, technology_summary_chain, technology_rating_chain, year_of_constr_chain, material_chain, \
    building_type_chain, number_floors_chain, monitoring_summary_chain, monitoring_rating_chain
from src.gpt.test.test_gpt import test_gpt
from src.gpt.test.tests import start_balcony_gpt_test, start_law_status_test, start_technology_test, \
    start_monitoring_test, start_basement_test, start_elevator_test, start_garage_test, start_garden_test, \
    start_kitchen_test, start_modernization_test, start_outbuilding_test

start_balcony_gpt_test(start=False)  # Success: 100%.
start_law_status_test(start=False)  # Success: 0.9473684210526315
start_technology_test(start=False)  # Success: 0.3928 - @TODO: divide the technology chain into smaller parts
start_monitoring_test(start=False)  # Success: 100%.
start_basement_test(start=True)  # 0.7857142857142857
start_elevator_test(start=False)
start_garage_test(start=False)
start_garden_test(start=False)
start_kitchen_test(start=False)
start_modernization_test(start=False)
start_outbuilding_test(start=False)
