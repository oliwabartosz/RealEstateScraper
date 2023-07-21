# SUMMARIES
balcony_prompt = """Analyze information about the balcony in the offer. "Don't treat french balcony as \
a balcony. 

French balcony (also called French balustrade, wallet) is a type of balcony limited only to the balcony window and \
balustrade.

If in the offer there is information that property has just the french balcony, treat that there is no balcony. \
Use maximum 2 sentences. 
Use information delimited by triple backticks: 
```{real_estate_offer_en}, {offer_parameters_en}```"""

technology_prompt = """Provide a two-sentence summary about technology of the building based on the information \
from this text: ```{real_estate_offer_en}```

The technology of the building can be traditional, improved, monolithic or prefabricated. The instruction
how to assess the technology is delimited by <>.

<The building technology is classified as:
- traditional when have brick construction until 1960, typically limited to 6 \
storeys, and comprising mainly of tenement houses and outbuildings.
- improved, when constructed using brick, silk, and blocks, with a year of construction greater than 1990.
- monolithic, pertains to tall buildings over 15 storeys built since 2007.
- prefabricated buildings were constructed using panel construction, large slabs, or concrete. They were constructed 
in years with range from 1960 to 1995. They can be high blocks with 10 to 12 storeys or low blocks up to 6 storeys>

While providing summary take also into consideration: 
- year of construction: ```{year_of_constr}```, 
- material ```{material}```, 
- building type: ```{building_type}```, 
- number of floors:  ```{number_of_floors}```.

Focus just on the building, skip the information about apartment.
"""

law_status_prompt = """Make a summary of the law status. The law status can be cooperative right or ownership \
right. Write if in text delimited in triple backticks there was mentioned about community or cooperative.

Use maximum three sentences. Tell your reasons.

Text to make summary from:
```{real_estate_offer_en}```
"""

elevator_prompt = """Make two sentences summary about elevator from text delimited in triple \
backticks. Does building have an elevator?  
```{real_estate_offer_en}```.
"""

basement_prompt = """Make two sentences summary about basement or attic from text delimited in triple \
backticks. Does basement or attic belong to the flat? Does it have additional price?  
```{real_estate_offer_en}````
"""

garage_prompt = """Make two sentences summary about garage and parking place from text delimited in triple \
backticks. Does garage or parking place belong to the flat? Does it have additional price? 
```{real_estate_offer_en}```
"""

garden_prompt = """Make two sentences summary about garden from text delimited in triple \
backticks. Does garden belong to the flat? Does it have additional price? 
```{real_estate_offer_en}```
"""

monitoring_prompt = """Make two sentences summary about monitoring from text delimited in triple backticks. \
Does building is monitored? Is it located in a guarded housing estate? Is there supervision and protection?
```{real_estate_offer_en}```
"""

kitchen_prompt = """Please provide a three-sentence summary about the kitchen based on the text enclosed \
in triple backticks. Could you describe what type of kitchen the apartment has and whether it is an annex? \
Additionally, mention if the kitchen has a window and is well-lit or if it lacks natural light and appears dark. \
 If there is no information about these details, kindly indicate so.
```{real_estate_offer_en}```
"""

rent_prompt = """What is the administrative rent based on text delimited in triple backticks.
```{real_estate_offer_en}```
"""

outbuilding_prompt = """Make two sentences summary about outbuilding from text delimited in triple backticks \
Is there any mention of outbuilding in the text? Does the text state that the building \
is located in the second line of development?
```{real_estate_offer_en}```
"""

modernization_prompt = """Provide a two-sentence summary of the building's modernization, based on the text \
enclosed in triple backticks. Has the building undergone insulation, modernization, or restoration? If so, \
please specify when these changes were made. Focus solely on information about the building and exclude any \
details about the apartment.
```{real_estate_offer_en}```
"""


