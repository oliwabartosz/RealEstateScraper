# RATINGS

technology_prompt = """Please rate the technology of the building based on the information provided in \
{technology_summary}.
- If the technology of the building is traditional, please return 1.
- If the technology of the building is traditional but improved, please return 2.
- If the technology of the building is monolithic, please return 3.
- If the building's material is prefabricated, please return 7.
- If it is not possible to determine the technology, please return -9.

Please provide a numeric response: 1, 2, 3, 7, or -9."""

law_status_prompt = """Please rate the legal status based on the information provided in {law_summary}.
- If the law status indicates ownership right, please return 1.
- If the law status indicates cooperative right, please return 2.
- If it is not possible to determine the legal status, please return -9.

Please provide a numeric response: 1, 2, or -9.
"""

balcony_prompt = """Please rate the presence of a balcony based on the information provided in {balcony_summary}.
- If there is a balcony, please return 1.
- If there is no balcony or if there is only a French balcony (without a full balcony), please return 0.
- If it is not possible to determine the presence of a balcony, please return -9.

Please provide a numeric response: 0, 1, or -9.
"""

elevator_prompt = """Please rate the presence of an elevator based on the information provided in {elevator_summary}
- If there is an elevator or building has more than 5 floors, please return 1.
- If there is no elevator or building has less than 5 floors, please return 0.
- If it is not possible to determine the presence of an elevator, please return -9.

Please provide a numeric response: 0, 1, or -9."""

basement_prompt = """Rate the occurrence of basement based on the information provided in {basement_summary}.
- If there is no basement or the basement comes with an additional price, please return 0.
- If there is a basement mentioned in the text without any information about the price, please return 1.
- If it is not possible to determine a rating, please return -9.

Return just number 0, 1 or -9."""

garage_prompt = """Please rate the occurrence of a garage or parking place based on the information provided in \
{garage_summary}.
- If there is no garage or parking place, or if it comes with an additional price, please return 0.
- If the garage or parking place belongs to the apartment without any information about the price, please return 1.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 0, 1, or -9."""

garden_prompt = """Please rate the occurrence of a garden  based on the information provided in \
{garden_summary}.
- If there is no garden, or if it comes with an additional price or is it unclear, please return 0.
- If the garden belongs to the apartment, please return 1.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 0, 1, or -9.
"""

monitoring_prompt = """Please rate the occurrence of monitoring based on the information provided in \
{monitoring_summary}.
- If there is no mention of monitoring, guarded estate, supervision, or protection, please return 0.
- If there is any mention of monitoring, guarded estate, supervision, or protection, please return 1.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 0, 1, or -9.
"""


kitchen_prompt = """Please rate the occurrence of a kitchen based on the information provided in {kitchen_summary}.
- If it has been mentioned that the kitchen is dark, please return 1.
- If it has been mentioned that the kitchen is bright, well-lit, or has a window, please return 2.
- If it has been mentioned that the kitchen is an annex, please return 3.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 1, 2, 3, or -9.
"""

rent_prompt = """Please provide a just numeric response that indicate the value of administrative rent from the \
information provided in {rent_summary}. 
If it is not possible to determine a rating, please return -9
"""

outbuilding_prompt = """
Please rate the occurrence of a outbuilding based on the information provided in {outbuilding_summary}. Take also \
information from ```technology_rating that is equal to {technology_rating}```.
- If it has been mentioned that building is outbuilding, please return 1.
- If it has been mentioned that building is located in the second line of development and technology_rating \
is 1, please return 1.
- If technology_rating is more than 1, please return 0.
- If it is not possible to determine a rating, please return 0.

Please provide a numeric response: 0, 1 or -9.
"""

modernization_prompt = """Please rate the modernization based on the information provided in \
{modernization_summary}.
Take also information from ```technology_rating that is equal to {technology_rating}```.

- If it has been mentioned that building was modernized, please return 4.
- If it has been mentioned that building is not modernized or will be modernized, please return 5.
- If technology rating is 2 or 3, please return null.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 4, 5, null or -9.
"""








