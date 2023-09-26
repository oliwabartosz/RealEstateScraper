from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain
from src.gpt.test.test_gpt import test_gpt

test_gpt([balcony_summary_chain, balcony_rating_chain],
         ["balcony_summary", "balcony_rating"],
         'test-balcony.json',
         verbose=True
         )
