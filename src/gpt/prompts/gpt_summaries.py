# SUMMARIES
balcony_prompt = """Using maximum 3 sentences answer the question: does text mention \
about balcony, terrace or loggia? \
If text says about french balcony or balcony window add this information to yours summary.\

Make a summary from text delimited by triple backticks (`): 
```{real_estate_offer_en}```"""

technology_prompt = """Provide a three-sentence summary about technology of the building based on the information \
from this text: ```{real_estate_offer_en}```

The technology of the building can be traditional, improved, monolithic or prefabricated. The instruction
how to assess the technology is delimited by <>.

<The building technology is classified as:
- traditional when have brick construction until 1960, typically limited to 6 \
storeys, and comprising mainly of tenement houses (kamienica) and outbuildings.
- improved, when constructed using brick, silk, silicate, silikat and blocks, with a year of construction greater than 1990.
- monolithic, pertains to tall buildings over 15 storeys built since 2007.
- prefabricated buildings were constructed using panel construction, large slabs (Wielka Płyta), Big Plate or concrete. They were constructed 
in years with range from 1960 to 1995. They can be high blocks with 10 to 12 storeys or low blocks up to 6 storeys>

In summary provide information of: 
- technology classification based on instruction delimited by <>
- year of construction: ```{year_of_constr}```, 
- material ```{material}```, 
- building type: ```{building_type}```, 
- number of floors:  ```{number_of_floors}```.

In summary ignore information if apartment was adaption of the attic. If year of construction is for prefabricated \
buildings but material is for traditional say it is hard to estimate the building technology.
Focus just on the building, skip the information about apartment.
"""

law_status_prompt = """Make a summary of the legal status. Does the text mention about cooperative ownership right \
(called alo social ownership) or ownership right?
Does text say that apartment is possible to buy by citizens from outside the European Union say that.

Use maximum three sentences. Tell your reasons.

Text to make summary from:
```{real_estate_offer_en}```
"""

elevator_prompt = """Make two sentences summary about elevator in the building from text delimited in triple \
backticks. Does building have an elevator?
```{real_estate_offer_en}```.
"""

basement_prompt_old = """Act as a text summarizer. Treat basement, attic, storage cell as a basement. Then make three \
sentences summary about basement from text delimited in triple backticks. The main question is: Does basement belong to \
the apartment? Give the answer to summary. 

Below are additional questions, but if there is no information about these, do not answer:
Does it have additional price or fee? It is in use for cooperative or public access?

Ignore information about garage or underground place. Try to look for a sentence: "The apartment has a basement."
If text doesn't mention whether basement belongs to the apartment or not do not include that information to summary.

Text to analyze:
```{real_estate_offer_en}````
"""

"""Using maximum 3 sentences answer the question: does text mention \
about balcony, terrace or loggia? \
If text says about french balcony or balcony window add this information to yours summary.\

Make a summary from text delimited by triple backticks (`): 
```{real_estate_offer_en}```"""

basement_prompt = """Using maximum 3 sentences answer the following question from the text delimited in triple \
backticks: does apartment includes used one of the following: basement, attic or storage room? Is there is an additional
for it? Is it for public use or belongs to apartment? 
In you answers don't provide information if text says that apartment is adaption of the attic.
   
Text to analyze:
```{real_estate_offer_en}```
"""

basement_prompt_old_2 = """. Then your task is to perform the following actions:
1. Find the information about the basement in text delimited in triple backticks (`).
2. Assess if basement is for additional price or fee - if there is no information treat that there is no additional price or fee.
3. Assess if basement is for use by the Cooperative or publicly accessible - if there is no information treat this is private.

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

monitoring_prompt = """Make three sentences summary about monitoring from text delimited in triple backticks. \
Does building or area near it is being monitored? Is building located in a guarded housing estate? Is there supervision or protection? \
Does text mentions something about monitoring?
If it is not possible to determine, say that. 
```{real_estate_offer_en}```
"""

kitchen_prompt = """Please provide a three-sentence summary about the kitchen based on the text enclosed \
in triple backticks. Could you describe what type of kitchen the apartment has and whether it is an annex? If kitchen \
is open to living room, say that there is an kitchen annex. \
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


