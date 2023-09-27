# RATINGS

technology_prompt = """Please rate the technology of the building based on the information provided in text delimited \
by three backticks (```)

Here is instruction how to rate the technology of the building:
- If the technology of the building is traditional, please return 1.
- If the technology of the building is traditional but improved, please return 2.
- If the technology of the building is monolithic, please return 3.
- If the building's material is prefabricated, please return 7.
- If it is not possible to determine the technology, please return -9.

Text to analyze:
```{technology_summary}```

Please provide a numeric response: 1, 2, 3, 7, or -9. Do not provide text!"""

law_status_prompt = """Please rate the legal status based on the information provided in text delimited by three backticks (```).
- If the legal status of an apartment is ownership return 1.
- If the legal status of an apartment is cooperative ownership right (it can be with the Land and Mortgage Register or KW), please return 2.
- If you don't know, please return -9.

Text to analyze:
```{law_summary}```

Examples of summaries and desired output is listed below delimited by three dashes (-).

---
Example:
Summary: The legal status of the property mentioned in the text is ownership. There is no mention of community or cooperation in the text.
Output: 1

Summary: The legal status of this property is the cooperative ownership right.
Output: 2 

Summary: The legal status of the property mentioned in the text is the right of cooperative ownership
Output: 2
---

Please provide a numeric response: 1, 2, or -9. Do not provide text!
"""

balcony_prompt = """Please rate the presence of a balcony, loggia or terrace based on the information provided in text delimited by three backticks (```). 
- If apartment has a balcony, terrace or loggia, please return 1.
- If apartment has not balcony, terrace or loggia please return 0.
- If apartment has just a French balcony or balcony window return 0,
- If it is not possible to determine the presence of a balcony, terrace or loggia (there is no inforamtion) \
please return -9.

Text to analyze:
```{balcony_summary}```.

Examples of summaries and desired output are listed below delimited by three dashes (-).

---
Example:
Summary: The apartment has a loggia, but there is no information provided about a balcony.
Output: 1

Summary: The apartment has a terrace, but there is no information provided about a balcony.
Output: 1

Summary: The apartment has a balcony window.
Output: 0

Summary: The apartment has a french balcony.
Output: 0

Summary: The apartment does not have a balcony, terrace, or loggia.
Output: 0

Summary: No information about balcony, terrace or loggia in text.
Output: -9
---
Please provide a numeric response: 0, 1, or -9. Do not provide text!
"""

elevator_prompt = """Please rate the presence of an elevator based on the information provided in {elevator_summary}
- If there is an elevator or building has more than 5 floors, please return 1.
- If there is no elevator or building has less than 5 floors, please return 0.
- If it is not possible to determine the presence of an elevator, please return -9.

Please provide a numeric response: 0, 1, or -9. Do not provide text!"""

basement_prompt = """Rate the occurrence of basement based on the information provided in {basement_summary}.
- If there is no basement or the basement comes with an additional price, please return 0.
- If there is a basement mentioned in the text without any information about the price, please return 1.
- If it is not possible to determine a rating, please return -9.

Return just number 0, 1 or -9. Do not provide text!"""

garage_prompt = """Please rate the occurrence of a garage or parking place based on the information provided in \
{garage_summary}.
- If there is no garage or parking place, or if it comes with an additional price, please return 0.
- If the garage or parking place belongs to the apartment without any information about the price, please return 1.
- If it is not possible to determine a rating, please return -9.

Examples of summaries and desired output is listed below delimited by three dashes (-).

---
Example:
Summary: The text mentions a garage that belongs to the apartment. The garage has an additional price of 80,000.
Output: 0

Summary: The text mentions a parking lot that belongs to the apartment. The parking lot has an additional price of 60 000.
Output: 0

Summary: The text mentions a garage that belongs to the apartment. The text does not mention about additional price.
Output: 1

Summary: The text mentions a parking lot that belongs to the apartment. The text does not mention about additional price.
Output: 1
---

Please provide a numeric response: 0, 1, or -9. Do not provide text!"""

garden_prompt = """Please rate the occurrence of a garden  based on the information provided in \
{garden_summary}.
- If there is no garden, or if it comes with an additional price or is it unclear, please return 0.
- If the garden belongs to the apartment, please return 1.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 0, 1, or -9. Do not provide text!
"""

monitoring_prompt = """Please rate the occurrence of monitoring based on the information provided in \
{monitoring_summary}.
- If there is no mention of monitoring, guarded estate, supervision, or protection, please return 0.
- If there is any mention of monitoring, guarded estate, supervision, or protection, please return 1.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 0, 1, or -9. Do not provide text!
"""


kitchen_prompt = """Please rate the occurrence of a kitchen based on the information provided in {kitchen_summary}.
- If it has been mentioned that the kitchen is dark, please return 1.
- If it has been mentioned that the kitchen is bright, well-lit, or has a window, please return 2.
- If it has been mentioned that the kitchen is an annex, please return 3.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 1, 2, 3, or -9. Do not provide text!
"""

rent_prompt = """Please provide a just numeric response that indicate the value of administrative rent from the \
information provided in {rent_summary}. Provide just number and skip the text.
If it is not possible to determine a rating, please return -9. Do not provide text!
"""

modernization_prompt = """Please rate the modernization based on the information provided in \
{modernization_summary}.
Take also information from ```technology_rating that is equal to {technology_rating}```.

- If it has been mentioned that building was modernized, please return 4.
- If it has been mentioned that building is not modernized or will be modernized, please return 5.
- If technology rating is 2 or 3, please return null.
- If it is not possible to determine a rating, please return -9.

Please provide a numeric response: 4, 5, null or -9. Do not provide text!
"""

outbuilding_prompt = """
Please rate the occurrence of a tenement house (called sometimes also outbuilding) based on the information provided \
in {outbuilding_summary}. Take also information from ```technology_rating that is equal to {technology_rating}```.
- If it has been mentioned that building is a tenement house, please return 1.
- If it has been mentioned that building is located in the second line of development and technology_rating \
is 1, please return 1.
- If technology_rating is more than 1, please return 0.
- If it is not possible to determine a rating, please return 0.

Please provide a numeric response: 0, 1 or -9. Do not provide text!
"""







