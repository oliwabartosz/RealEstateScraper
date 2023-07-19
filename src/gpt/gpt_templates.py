# TRANSLATION PROMPTS
translate_description_prompt = """Translate the following real estate offer from polish to english: \
{real_estate_offer}"""

translate_params_prompt = """Translate the following real estate parameters from polish to english:
{offer_parameters}"""

# SUMMARIES
balcony_summary_prompt = """Analyze information about the balcony in the offer. "Don't treat french balcony as \
a balcony. 
    
French balcony (also called French balustrade, wallet) is a type of balcony limited only to the balcony window and \
balustrade.
    
If in the offer there is information that property has just the french balcony, treat that there is no balcony. \
Use maximum 2 sentences. 
Use information delimited by triple backticks: 
```{real_estate_offer_en}, {offer_parameters_en}```"""

technology_summary_prompt = """Make a summary of the technology of the building, year of construction, material, \
building type and number of floors of the building. Also analyze if technology of the building is traditional, \
traditional improved, monolithic or prefabricated. 

Buildings based on traditional technology are buildings built of brick until 1960. As a rule, they do not exceed \
6 storeys. These are mostly tenement houses and outbuildings. They arent constructed using panel construction.

Buildings based on traditional improved technology are built of brick, silk and blocks. The year of \
construction is greater than 1990."

Buildings based on monolithic technology are tall buildings, over 15 storeys, built since 2007.

Buildings based on prefabricated technology constructed using panel construction, large slabs or concrete. \
They are high blocks with 10 to 12 storeys but can also be a low blocks up to 6 storeys. Year of construction is from \
1960 to 1995.

Write up to maximum 3 sentences. Give especially information what technology is.

Use information delimited by triple backticks  
```{real_estate_offer_en}, {offer_parameters_en}, {year_of_constr}, {material}, {building_type}, {number_of_floors}``` \
"""

law_status_summary_prompt = """Make a summary of the law status. The law status can be cooperative right or ownership \
right. Write if in text delimited in triple backticks there was mentioned about community or cooperative.

Use maximum three sentences. Tell your reasons.

Text to make summary from:
```{real_estate_offer_en}```
"""

elevator_summary_prompt = """Extract information about elevator from text delimited in \
triple backticks:
```{real_estate_offer_en}```

Then take information from {elevator}.

Based on information above make a statement if there is an elevator in the building.
"""

# RATINGS

technology_rating_prompt = """
Rate the technology based on {technology_summary}.
- if technology of the building is traditional return 1.
- if technology of the building is traditional improved return 2.
- if technology of the building is monolithic return 3. 
- if material is prefabricated return 7.
- return -9 if it's not possible to rate.

Return just a number 1, 2, 3, 7 or -9."""

law_status_rating_prompt = """
Rate the law status based on {law_summary}.
- if law status is ownership right return 1.
- if law status is cooperative right return 2.
- if it's not possible to rate, return -9. 

Return just number 1, 2 or -9.
"""

balcony_rating_prompt = """
Rate the balcony based on {balcony_summary}.
- if there is balcony return 1.
- if there isn't balcony return 0.
- if it's not possible to rate, return -9. 

Return just number 0, 1 or -9.
"""

elevator_rating_prompt = """
Rate the elevator based on on {elevator_summary}.
- If there is elevator return 1.
- If there isn't elevator return 0.
- If it's not possible to rate, return -9. 

Return just number 0, 1 or -9."""


# PARAMETERS
year_of_constr_prompt = """Get the year of the construction from text below:
{offer_parameters_en}
    
If there were no information, take then from text below:
{real_estate_offer_en}"""

building_type_prompt = """Get the building type from text below:
{offer_parameters_en}

If there were no information, take then from text below:
{real_estate_offer_en}"""

material_prompt = """Get the material from text below:
{offer_parameters_en}

If there were no information, take then from text below:"
{real_estate_offer_en}"""

number_floors_prompt = """Get the number of floors from text below:"
{offer_parameters_en}"

If there were no information, take then from text below:"
{real_estate_offer_en}

Add 1 to the number of floors.
"""

elevator_prompt = """
Get the information about elevator from the text below:"
{offer_parameters_en}"

If there were no information provided say that.
"""


