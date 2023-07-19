from src.config import config_data
from operator import itemgetter

from src.gpt import gpt_templates
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

# 1. TRANSLATION

# Translating description from PL to EN
translate_desc_prompt = ChatPromptTemplate.from_template(gpt_templates.translate_description_prompt)
translate_desc_chain = LLMChain(llm=llm, prompt=translate_desc_prompt, output_key="real_estate_offer_en")

# Translating parameters from PL to EN
translate_params_prompt = ChatPromptTemplate.from_template(gpt_templates.translate_params_prompt)
translate_params_chain = LLMChain(llm=llm, prompt=translate_params_prompt, output_key="offer_parameters_en")

# PARAMETERS

# Year of the construction of the building
year_of_constr_prompt = ChatPromptTemplate.from_template(gpt_templates.year_of_constr_prompt)
year_of_constr_chain = LLMChain(llm=llm, prompt=year_of_constr_prompt, output_key="year_of_constr")

# Building type
building_type_prompt = ChatPromptTemplate.from_template(gpt_templates.building_type_prompt)
building_type_chain = LLMChain(llm=llm, prompt=building_type_prompt, output_key="building_type")

# Material of the building that have been constructed
material_prompt = ChatPromptTemplate.from_template(gpt_templates.material_prompt)
material_chain = LLMChain(llm=llm, prompt=material_prompt, output_key="material")

# Number of floors that building have
number_floors_prompt = ChatPromptTemplate.from_template(gpt_templates.number_floors_prompt)
number_floors_chain = LLMChain(llm=llm, prompt=number_floors_prompt, output_key="number_of_floors")

# Elevator
elevator_prompt = ChatPromptTemplate.from_template(gpt_templates.elevator_prompt)
elevator_chain = LLMChain(llm=llm, prompt=elevator_prompt, output_key="elevator")

# SUMMARIES & RATINGS

# Technology
technology_summary_prompt = ChatPromptTemplate.from_template(gpt_templates.technology_summary_prompt)
technology_summary_chain = LLMChain(llm=llm, prompt=technology_summary_prompt, output_key="technology_summary")

# Law status
law_status_summary_prompt = ChatPromptTemplate.from_template(gpt_templates.law_status_summary_prompt)
law_status_summary_chain = LLMChain(llm=llm, prompt=law_status_summary_prompt, output_key="law_summary")

# Balcony
balcony_summary_prompt = ChatPromptTemplate.from_template(gpt_templates.balcony_summary_prompt)
balcony_summary_chain = LLMChain(llm=llm, prompt=balcony_summary_prompt, output_key="balcony_summary")

# Elevator
elevator_summary_prompt = ChatPromptTemplate.from_template(gpt_templates.elevator_summary_prompt)
elevator_summary_chain = LLMChain(llm=llm, prompt=elevator_summary_prompt, output_key="elevator_summary")

# Basement

# Garage

# Garden

# Monitoring

# Kitchen

# Rent

# Outbuilding

# Modernization

# RATINGS

# Technology
technology_rating_prompt = ChatPromptTemplate.from_template(gpt_templates.technology_rating_prompt)
technology_rating_chain = LLMChain(llm=llm, prompt=technology_rating_prompt, output_key="technology_rating")

# Law status
law_status_rating_prompt = ChatPromptTemplate.from_template(gpt_templates.law_status_rating_prompt)
law_status_rating_chain = LLMChain(llm=llm, prompt=law_status_rating_prompt, output_key="law_rating")

# Balcony
balcony_rating_prompt = ChatPromptTemplate.from_template(gpt_templates.balcony_rating_prompt)
balcony_rating_chain = LLMChain(llm=llm, prompt=balcony_rating_prompt, output_key="balcony_rating")

# Elevator
elevator_rating_prompt = ChatPromptTemplate.from_template(gpt_templates.elevator_rating_prompt)
elevator_rating_chain = LLMChain(llm=llm, prompt=elevator_rating_prompt, output_key="elevator_rating")

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
    chains=[
        translate_desc_chain, translate_params_chain,
        year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
        technology_summary_chain, technology_rating_chain,
        balcony_summary_chain, balcony_rating_chain,
        law_status_summary_chain, law_status_rating_chain,
        elevator_chain, elevator_summary_chain, elevator_rating_chain
    ],
    input_variables=["real_estate_offer", "offer_parameters"],
    output_variables=[
        "offer_parameters_en", "real_estate_offer_en",
        "technology_summary", "technology_rating",
        "balcony_summary", "balcony_rating",
        "law_summary", "law_rating",
        "elevator", "elevator_summary", "elevator_rating",
        "number_of_floors", ],
    verbose=True
)

parameters = """
<Materiał>: Wielka płyta
<Rodzaj budynku>: Blok
<Rok budowy> 1983
<Balkon> Tak
<Liczba kondygnacji> 4
<Piwnica> Nie
<Kuchnia> Oddzielna
<Czynsz> 750
"""

offer_description = """
<Opis mieszkania> Ofertą sprzedaży jest dwupokojowe mieszkanie zlokalizowane na obrzeżach Szczecina.Lokal jest w bardzo dobrym stanie, umeblowanie pozostaje także jest gotowy do zamieszkania. Obecni właściciele 3 lata temu przeprowadzili generalny remont, zostały powymieniane wszystkie instalacje, umieszczono nowe wyposażenie -samo mieszkanie jest zadbane i nie wymaga żadnych nakładów finansowych.Powierzchnia wynosi 47,7m² i składa się z jasnego salonu z balkonem francuskim, drugiego pokoju i przedpokoju z pojemną szafą. Łazienka jest z wanna oraz osobnym WC, a kuchnia jest oddzielna oraz wyposażona w zmywarkę, piekarnik, lodówkę oraz płytę indukcyjną. Aktualny układ mieszkania pozwala na połączenie pomieszczeń w celu otwarcia większej przestrzeni oraz aranżacji według własnego stylu. W budynku jest winda. Pod budynkiem znajduje się wiele miejsc parkingowych dzięki czemu nigdy nie ma problemu z parkowaniem, a w pobliżu są również przystanki autobusowe dla osób niezmotoryzowanych. Sama okolica jest cicha i spokojna - idealna dla osób, które sobie cenią te atuty. Mieszkanie znajduje się na obrzeżach miasta, gdzie jest blisko do wylotówki na autostradę jednak dojazd do centrum Szczecina zajmuje 10/15 minut. Natomiast w pobliżu jest wiele punktów handlowych i usługowych m.in. galerie handlowe, restauracje, kino, sklepy czy plac zabaw. Jeśli pracujesz poza miastem i potrzebujesz mieszkania blisko obwodnicy lub szukasz czegoś z dala od miejskiego zgiełku ta oferta jest idealna dla Ciebie. Szczególnie polecam singlom czy parze bez dzieci. Serdecznie zapraszam do kontaktu w celu obejrzenia mieszkania.
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
