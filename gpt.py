from src.config import config_data
from operator import itemgetter
from src.handlers.file_handler import load_txt_file, save_txt_file, FILE_PATH_GPT_INPUT, FILE_PATH_GPT_OUTPUT

# Langchain imports
from langchain.llms import OpenAI
from langchain.chains import SequentialChain

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Load model

data = config_data.get_config_data()
text = load_txt_file(FILE_PATH_GPT_INPUT)
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(data)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0, )

# Chaining...


# TRANSLATION

# PROMPT: Translation offer description from PL to EN
translate_desc_prompt = ChatPromptTemplate.from_template(
    "Translate the following real estate offer from polish to english:"
    "\n\n{real_estate_offer}"
)

# CHAIN: input= real_estate_offer and output= real_estate_offer_en
translate_desc_chain = LLMChain(llm=llm, prompt=translate_desc_prompt,
                                output_key="real_estate_offer_en"
                                )

# PROMPT: Translation offer parameters from PL to EN
translate_params_prompt = ChatPromptTemplate.from_template(
    "Translate the following real estate parameters from polish to english:"
    "\n\n{offer_parameters}"
)

# CHAIN: input= offer_parameters and output= offer_parameters_en
translate_params_chain = LLMChain(llm=llm, prompt=translate_params_prompt,
                                  output_key="offer_parameters_en"
                                  )

# PARAMETERS

# PROMPT: Take the Year of construction from params
year_of_constr_prompt = ChatPromptTemplate.from_template(
    "Get the year of the construction from:"
    "\n\n{offer_parameters_en}"
    "If there is no information {offer_parameters_en}, take then from:"
    "\n\n{real_estate_offer_en}"
)

# CHAIN: input= offer_parameters_en and output= year_of_constr
year_of_constr_chain = LLMChain(llm=llm, prompt=year_of_constr_prompt,
                                output_key="year_of_constr"
                                )

# PROMPT: Take the material from params
material_prompt = ChatPromptTemplate.from_template(
    "Get the material from:"
    "\n\n{offer_parameters_en}"
    "If there is no information {offer_parameters_en}, take then from:"
    "\n\n{real_estate_offer_en}"
)

# CHAIN: input= offer_parameters_en and output= material
material_chain = LLMChain(llm=llm, prompt=material_prompt,
                          output_key="material"
                          )

# PROMPT: Take the number of floors from params
number_floors_prompt = ChatPromptTemplate.from_template(
    "Get the number of floors from:"
    "\n\n{offer_parameters_en}"
    "If there is no information {offer_parameters_en}, take then from:"
    "\n\n{real_estate_offer_en}"
)

# CHAIN: input= offer_parameters_en and output= number_of_floors
number_floors_chain = LLMChain(llm=llm, prompt=number_floors_prompt,
                               output_key="number_of_floors"
                               )

# PROMPT: Get summary of the technology of the building, year of const,
technology_summary_prompt = ChatPromptTemplate.from_template(
    "Summerize within maximum of 2 sentences the technology, year of construction, material and number of floors of the building "
    "from:"
    "\n\n{real_estate_offer_en}, {year_of_constr}, {material}, {number_of_floors}"

)

# CHAIN: input= English_Review and output= summary
technology_summary_chain = LLMChain(llm=llm, prompt=technology_summary_prompt,
                                    output_key="technology_summary"
                                    )
# PROMPT: Rate the technology using nominal scale
technology_rating_prompt = ChatPromptTemplate.from_template(
    """Rate the technology of the building in using the nominal scale and the year of construction is less than. 
       Return 1 if material, which is {material} is brick or year of construction, which is {year_of_constr} is less than 1960.
       Return 2 if material, which is {material} is brick  or year of construction, which is {year_of_constr} is more than 2000.
       Return 3 if number of floors, which is {number_of_floors} is more than 15. 
       Return 7 if material, which is {material} is large slabs or concrete or other and or year of construction, which is {year_of_constr} is between 1960 and 1992.
       Return -9 if it's not possible to rate.
       
       Make a rating on this text:          
    \n\n{technology_summary}
    \n\n Return just a number 1, 2, 3, 7 or -9.
    """
)

# chain 3: input= Review and output= language
technology_rating_chain = LLMChain(llm=llm, prompt=technology_rating_prompt,
                                   output_key="technology_rating"
                                   )

# # Generate JSON file.
# json_prompt = ChatPromptTemplate.from_template(
#     """
#     Provide a JSON object, that have key technology_GPT.
#     The value of technology_GPT is {technology_rating}
#     """
#
# )
# # chain 4: input= summary, language and output= followup_message
# json_chain = LLMChain(llm=llm, prompt=json_prompt,
#                       output_key="JSON"
#                       )

# overall_chain: input= Review
# and output= English_Review,summary, followup_message
overall_chain = SequentialChain(
    chains=[translate_desc_chain, translate_params_chain, year_of_constr_chain, material_chain, number_floors_chain,
            technology_summary_chain, technology_rating_chain],
    input_variables=["real_estate_offer", "offer_parameters"],
    output_variables=["real_estate_offer_en", "technology_summary", "technology_rating", "offer_parameters_en"],
    verbose=True
)

parameters = """
<Materiał>: Cegła
<Rok budowy> 1927
<Stan prawny> Własność
<Balkon> Nie
<Winda> Nie
<Liczba kondygnacji> 5
<Piwnica> Nie
<Kuchnia> Oddzielna
<Czynsz> 300
"""

offer_description = """
<Opis mieszkania> Do wynajęcia 2 pokojowe mieszkanie usytuowane na Pogodnie. Mieszkanie znajduje się na 2 piętrze w odnowionym, niewielkim ( 4 rodzinnym ) budynku. Na powierzchni ok 43m2 znajdują się 2 pokoje o pow. ok. 10 i 15m2, duża 14m2 kuchnia i łazienka z wc. Mieszkanie jest umeblowane i wyposażone w sprzęt AGD. Ogrzewanie i ciepła woda z pieca gazowego 2obiegowego.Opłaty: czynsz ok. 325 zł, gaz ok. 150 zł 1/m-c, prąd ok 90 zł 1/m-c.Cały dom jest ocieplony styropianem a dach wełna mineralną. Okna PCV.Przed domem jest możliwość zaparkowania auta. Można również korzystać z ogrodu dostępnego wyłącznie dla meiszkańców domu.Serdecznie polecam i zapraszam na prezentację.
"""

print(overall_chain({'real_estate_offer': offer_description, "offer_parameters": parameters}))

#############################################

# from langchain.chat_models import ChatOpenAI
# from langchain.schema import (
#     AIMessage,
#     HumanMessage,
#     SystemMessage
# )
#
# data = config_data.get_config_data()
# text = load_txt_file(FILE_PATH_GPT_INPUT)
# OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(data)
#
# # llm = OpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)
# # answer = llm.predict(text)
# # print(answer)
#
#
# chat = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0)
# answer = chat.predict_messages([HumanMessage(content=f"{text}")])
#
# save_txt_file(FILE_PATH_GPT_OUTPUT, answer.content)
# print("Done.")
