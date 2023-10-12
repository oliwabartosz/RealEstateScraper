import sys

from src.gpt.test.test_gpt import test_gpt, insert_results_to_df
from src.scrapper import questions
from src.gpt.gpt import start_gpt_assessment

print(sys.path)

if __name__ == "__main__":
    # Initial questions
    offers_type = questions.type_of_offers()
    retry = questions.retry_gpt()

    start_gpt_assessment(start=0, end=None, retry=retry, offers_type=offers_type)

