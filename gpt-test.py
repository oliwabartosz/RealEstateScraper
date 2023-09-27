from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain, law_status_summary_chain, \
    law_status_rating_chain, technology_summary_chain, technology_rating_chain, year_of_constr_chain, material_chain, \
    building_type_chain, number_floors_chain
from src.gpt.test.test_gpt import test_gpt

# print('Balcony:')
# test_gpt([balcony_summary_chain, balcony_rating_chain],
#          ["balcony_summary", "balcony_rating"],
#          False,
#          'test-balcony.json',
#          True
#          )
#
# print('lawStatus:')
# test_gpt([law_status_summary_chain, law_status_rating_chain],
#          ["law_summary", "law_rating"],
#          True,
#          'test-law-status.json',
#          True
#          )

print('technology:')
test_gpt([year_of_constr_chain, material_chain, building_type_chain, number_floors_chain, technology_summary_chain,
          technology_rating_chain],
         ["technology_summary", "technology_rating"],
         True,
         'test-technology.json',
         True
         )
