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
building_type_prompt = ChatPromptTemplate.from_template(
    "Get the building type from:"
    "\n\n{offer_parameters_en}"
    "If there is no information {offer_parameters_en}, take then from:"
    "\n\n{real_estate_offer_en}"
)

# CHAIN: input= offer_parameters_en and output= material
building_type_chain = LLMChain(llm=llm, prompt=building_type_prompt,
                               output_key="building_type"
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
    "Make a summary of the technology of the building, year of construction, material, building type and number of floors of the building "
    "Also try to analyze if technology of the building is traditional, traditional improved, monolithic, prefabricated."
    "\nBuildings based on traditional technology are buildings built of brick until 1960. As a rule, they do not exceed 6 storeys. These are mostly tenement houses and outbuildings. They arent constructed using panel construction."
    "\nBuildings based on traditional improved technology are mainly buildings built of brick, silk and blocks since 1990."
    "\nBuildings based on monolithic technology are tall buildings, over 15 storeys, built since 2007."
    "\nBuildings based on prefabricated technology are high blocks with 10 to 12 storeys or low blocks up to 6 storeys built in the years 1960-1995 constructed using panel construction, large slab or concrete."
    "\nWrite up to maximum 3 sentences. Give especially information what technology is."
    "\n\n"
    "Use information delimited by triple backticks"
    "\n\n```{real_estate_offer_en}, {offer_parameters_en}, {year_of_constr}, {material}, {building_type}, {number_of_floors}```"

)

# CHAIN: input= English_Review and output= summary
technology_summary_chain = LLMChain(llm=llm, prompt=technology_summary_prompt,
                                    output_key="technology_summary"
                                    )
# PROMPT: Rate the technology using nominal scale with comment
technology_rating_prompt = ChatPromptTemplate.from_template(
    """Rate the technology based on {technology_summary}.\n
       - if technology of the building is traditional return 1.\n
       - if technology of the building is traditional improved return 2.\n
       - if technology of the building is monolithic return 3. \n
       - if material is prefabricated return 7.\n.
       - return -9 if it's not possible to rate\n\n.
  
    \n\n Return just a number 1, 2, 3, 7 or -9.
    """
)

# CHAIN: input= technology_rating_prompt and output= technology_rating_comment
technology_rating_chain = LLMChain(llm=llm, prompt=technology_rating_prompt,
                                   output_key="technology_rating"
                                   )



# BALCONY

balcony_summary_prompt = ChatPromptTemplate.from_template(
    "Analyze information about the balcony in the offer."
    "Don't treat french balcony as a balcony. French balcony (also called French balustrade, wallet) is a type of balcony limited only to the balcony window and balustrade"
    "If in the offer there is information that property has the french balcony, write there is no balcony"
    "Use information delimited by triple backticks"
    "\n\n```{real_estate_offer_en}, {offer_parameters_en}```"

)

# CHAIN: input= English_Review and output= summary
balcony_summary_chain = LLMChain(llm=llm, prompt=balcony_summary_prompt,
                                    output_key="balcony_summary"
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
    chains=[translate_desc_chain, translate_params_chain,
            year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
            technology_summary_chain, technology_rating_chain,
            balcony_summary_chain],
    input_variables=["real_estate_offer", "offer_parameters"],
    output_variables=["offer_parameters_en", "technology_summary", "technology_rating", "balcony_summary"],
    verbose=True
)

parameters = """
<Materiał>: Cegła
<Rodzaj budynku>: Blok
<Rok budowy> 1983
<Stan prawny> Spółdzielcze własnościowe prawo
<Balkon> Tak
<Winda> Nie
<Liczba kondygnacji> 4
<Piwnica> Nie
<Kuchnia> Oddzielna
<Czynsz> 750
"""

offer_description = """
<Opis mieszkania> Ofertą sprzedaży jest dwupokojowe mieszkanie zlokalizowane na obrzeżach Szczecina.Lokal jest w bardzo dobrym stanie, umeblowanie pozostaje także jest gotowy do zamieszkania. Obecni właściciele 3 lata temu przeprowadzili generalny remont, zostały powymieniane wszystkie instalacje, umieszczono nowe wyposażenie -samo mieszkanie jest zadbane i nie wymaga żadnych nakładów finansowych.Powierzchnia wynosi 47,7m² i składa się z jasnego salonu z balkonem francuskim, drugiego pokoju i przedpokoju z pojemną szafą. Łazienka jest z wanna oraz osobnym WC, a kuchnia jest oddzielna oraz wyposażona w zmywarkę, piekarnik, lodówkę oraz płytę indukcyjną. Aktualny układ mieszkania pozwala na połączenie pomieszczeń w celu otwarcia większej przestrzeni oraz aranżacji według własnego stylu. Pod budynkiem znajduje się wiele miejsc parkingowych dzięki czemu nigdy nie ma problemu z parkowaniem, a w pobliżu są również przystanki autobusowe dla osób niezmotoryzowanych. Sama okolica jest cicha i spokojna - idealna dla osób, które sobie cenią te atuty. Mieszkanie znajduje się na obrzeżach miasta, gdzie jest blisko do wylotówki na autostradę jednak dojazd do centrum Szczecina zajmuje 10/15 minut. Natomiast w pobliżu jest wiele punktów handlowych i usługowych m.in. galerie handlowe, restauracje, kino, sklepy czy plac zabaw. Jeśli pracujesz poza miastem i potrzebujesz mieszkania blisko obwodnicy lub szukasz czegoś z dala od miejskiego zgiełku ta oferta jest idealna dla Ciebie. Szczególnie polecam singlom czy parze bez dzieci. Serdecznie zapraszam do kontaktu w celu obejrzenia mieszkania.
"""
print(overall_chain({'real_estate_offer': offer_description, "offer_parameters": parameters}), end='\n')

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
