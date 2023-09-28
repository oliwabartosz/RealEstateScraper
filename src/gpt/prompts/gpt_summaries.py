# SUMMARIES
balcony_prompt = """Using maximum 3 sentences, make a short summary about if the apartment has balcony, terrace, loggia or don't have. \
If text doesn't mention about balcony, terrace, loggia, say that. If text says about french balcony or balcony window add this information to yours summary. 
Use information below from text delimited by triple backticks (`): 
```{real_estate_offer_en}```"""

technology_prompt = """Provide a three-sentence summary about technology of the building based on the information \
from this text: ```{real_estate_offer_en}```

The technology of the building can be traditional, improved, monolithic or prefabricated. The instruction
how to assess the technology is delimited by <>.

<The building technology is classified as:
- traditional when have brick construction until 1960, typically limited to 6 \
storeys, and comprising mainly of tenement houses (kamienica) and outbuildings.
- improved, when constructed using brick, silk, and blocks, with a year of construction greater than 1990.
- monolithic, pertains to tall buildings over 15 storeys built since 2007.
- prefabricated buildings were constructed using panel construction, large slabs (Wielka Płyta), or concrete. They were constructed 
in years with range from 1960 to 1995. They can be high blocks with 10 to 12 storeys or low blocks up to 6 storeys>

In summary provide information of: 
- technology classification based on instruction delimited by <>
- year of construction: ```{year_of_constr}```, 
- material ```{material}```, 
- building type: ```{building_type}```, 
- number of floors:  ```{number_of_floors}```.

Focus just on the building, skip the information about apartment.
"""

law_status_prompt = """Make a summary of the legal status. The legal status can be \
cooperative ownership right or ownership right. Write which legal status is for this apartment.

Use maximum three sentences. Tell your reasons.

Text to make summary from:
```{real_estate_offer_en} and {offer_parameters_en}```
"""

elevator_prompt = """Make two sentences summary about elevator in the building from text delimited in triple \
backticks. Does building have an elevator? How many floors the building has?  
```{real_estate_offer_en}```.
"""

basement_prompt = """Make two sentences summary about basement or attic from text delimited in triple \
backticks. Does basement or attic belong to the flat? Does it have additional price?  
```{real_estate_offer_en}````
"""

garage_prompt = """Make three sentences summary about garage and parking place from text delimited in triple \
backticks. Does garage or parking place belong to the apartment? Does it have additional price? Does the text mention \
that is to possible to buy garage or parking place? 
```{real_estate_offer_en}```
"""

garden_prompt = """Make two sentences summary about garden from text delimited in triple \
backticks. Does garden belong to the flat? Does it have additional price? If the garden is located on loggia or terrace
treat that information as there is no garden at all.
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
details about the apartment. Do not make summary of apartment modernization.
```{real_estate_offer_en}```
"""


