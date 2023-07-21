from src.config import config_data
from operator import itemgetter

from src.gpt.templates import gpt_translation, gpt_params, gpt_summaries, gpt_ratings
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
translate_desc_prompt = ChatPromptTemplate.from_template(gpt_translation.translate_description_prompt)
translate_desc_chain = LLMChain(llm=llm, prompt=translate_desc_prompt, output_key="real_estate_offer_en")

# Translating parameters from PL to EN
translate_params_prompt = ChatPromptTemplate.from_template(gpt_translation.translate_params_prompt)
translate_params_chain = LLMChain(llm=llm, prompt=translate_params_prompt, output_key="offer_parameters_en")

# PARAMETERS

# Year of the construction of the building
year_of_constr_prompt = ChatPromptTemplate.from_template(gpt_params.year_of_constr_prompt)
year_of_constr_chain = LLMChain(llm=llm, prompt=year_of_constr_prompt, output_key="year_of_constr")

# Building type
building_type_prompt = ChatPromptTemplate.from_template(gpt_params.building_type_prompt)
building_type_chain = LLMChain(llm=llm, prompt=building_type_prompt, output_key="building_type")

# Material of the building that have been constructed
material_prompt = ChatPromptTemplate.from_template(gpt_params.material_prompt)
material_chain = LLMChain(llm=llm, prompt=material_prompt, output_key="material")

# Number of floors that building have
number_floors_prompt = ChatPromptTemplate.from_template(gpt_params.number_floors_prompt)
number_floors_chain = LLMChain(llm=llm, prompt=number_floors_prompt, output_key="number_of_floors")

# Elevator
elevator_prompt = ChatPromptTemplate.from_template(gpt_params.elevator_prompt)
elevator_chain = LLMChain(llm=llm, prompt=elevator_prompt, output_key="elevator")

# SUMMARIES

# Technology
technology_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.technology_prompt)
technology_summary_chain = LLMChain(llm=llm, prompt=technology_summary_prompt, output_key="technology_summary")

# Law status
law_status_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.law_status_prompt)
law_status_summary_chain = LLMChain(llm=llm, prompt=law_status_summary_prompt, output_key="law_summary")

# Balcony
balcony_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.balcony_prompt)
balcony_summary_chain = LLMChain(llm=llm, prompt=balcony_summary_prompt, output_key="balcony_summary")

# Elevator
elevator_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.elevator_prompt)
elevator_summary_chain = LLMChain(llm=llm, prompt=elevator_summary_prompt, output_key="elevator_summary")

# Basement
basement_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.basement_prompt)
basement_summary_chain = LLMChain(llm=llm, prompt=basement_summary_prompt, output_key="basement_summary")

# Garage
garage_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.garage_prompt)
garage_summary_chain = LLMChain(llm=llm, prompt=garage_summary_prompt, output_key="garage_summary")

# Garden
garden_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.garden_prompt)
garden_summary_chain = LLMChain(llm=llm, prompt=garden_summary_prompt, output_key="garden_summary")

# Monitoring
monitoring_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.monitoring_prompt)
monitoring_summary_chain = LLMChain(llm=llm, prompt=monitoring_summary_prompt, output_key="monitoring_summary")

# Kitchen
kitchen_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.kitchen_prompt)
kitchen_summary_chain = LLMChain(llm=llm, prompt=kitchen_summary_prompt, output_key="kitchen_summary")

# Rent
rent_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.rent_prompt)
rent_summary_chain = LLMChain(llm=llm, prompt=rent_summary_prompt, output_key="rent_summary")

# Outbuilding
outbuilding_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.outbuilding_prompt)
outbuilding_summary_chain = LLMChain(llm=llm, prompt=outbuilding_summary_prompt, output_key="outbuilding_summary")

# Modernization
modernization_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.modernization_prompt)
modernization_summary_chain = LLMChain(llm=llm, prompt=modernization_summary_prompt, output_key="modernization_summary")

# RATINGS

# Technology
technology_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.technology_prompt)
technology_rating_chain = LLMChain(llm=llm, prompt=technology_rating_prompt, output_key="technology_rating")

# Law status
law_status_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.law_status_prompt)
law_status_rating_chain = LLMChain(llm=llm, prompt=law_status_rating_prompt, output_key="law_rating")

# Balcony
balcony_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.balcony_prompt)
balcony_rating_chain = LLMChain(llm=llm, prompt=balcony_rating_prompt, output_key="balcony_rating")

# Elevator
elevator_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.elevator_prompt)
elevator_rating_chain = LLMChain(llm=llm, prompt=elevator_rating_prompt, output_key="elevator_rating")

# Basement
basement_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.basement_prompt)
basement_rating_chain = LLMChain(llm=llm, prompt=basement_rating_prompt, output_key="basement_rating")

# Garage
garage_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.garage_prompt)
garage_rating_chain = LLMChain(llm=llm, prompt=garage_rating_prompt, output_key="garage_rating")

# Garden
garden_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.garden_prompt)
garden_rating_chain = LLMChain(llm=llm, prompt=garden_rating_prompt, output_key="garden_rating")

# Monitoring
monitoring_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.monitoring_prompt)
monitoring_rating_chain = LLMChain(llm=llm, prompt=monitoring_rating_prompt, output_key="monitoring_rating")

# Kitchen
kitchen_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.kitchen_prompt)
kitchen_rating_chain = LLMChain(llm=llm, prompt=kitchen_rating_prompt, output_key="kitchen_rating")

# Rent
rent_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.rent_prompt)
rent_rating_chain = LLMChain(llm=llm, prompt=rent_rating_prompt, output_key="rent_rating")

# Outbuilding
outbuilding_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.outbuilding_prompt)
outbuilding_rating_chain = LLMChain(llm=llm, prompt=outbuilding_rating_prompt, output_key="outbuilding_rating")

# Modernization
modernization_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.modernization_prompt)
modernization_rating_chain = LLMChain(llm=llm, prompt=modernization_rating_prompt, output_key="modernization_rating")


overall_chain = SequentialChain(
    chains=[
        translate_desc_chain, translate_params_chain,
        year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
        technology_summary_chain, technology_rating_chain,
        balcony_summary_chain, balcony_rating_chain,
        law_status_summary_chain, law_status_rating_chain,
        elevator_chain, elevator_summary_chain, elevator_rating_chain,
        basement_summary_chain, basement_rating_chain,
        garage_summary_chain, garage_rating_chain,
        garden_summary_chain, garden_rating_chain,
        monitoring_summary_chain, monitoring_rating_chain,
        kitchen_summary_chain, kitchen_rating_chain,
        rent_summary_chain, rent_rating_chain,
        outbuilding_summary_chain, outbuilding_rating_chain,
        modernization_summary_chain, modernization_rating_chain
    ],
    input_variables=["real_estate_offer", "offer_parameters"],
    output_variables=[
        "offer_parameters_en", "real_estate_offer_en",
        "technology_summary", "technology_rating",
        "balcony_summary", "balcony_rating",
        "law_summary", "law_rating",
        "elevator", "elevator_summary", "elevator_rating",
        "basement_summary", "basement_rating",
        "garage_summary", "garage_rating",
        "garden_summary", "garden_rating",
        "monitoring_summary", "monitoring_rating",
        "kitchen_summary", "kitchen_rating",
        "rent_summary", "rent_rating",
        "outbuilding_summary", "outbuilding_rating",
        "modernization_summary", "modernization_rating",
    ],
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
<Opis mieszkania> Ofertą sprzedaży jest dwupokojowe mieszkanie zlokalizowane na obrzeżach Szczecina.Lokal jest w bardzo dobrym stanie, \
umeblowanie pozostaje także jest gotowy do zamieszkania. Obecni właściciele 3 lata temu przeprowadzili generalny remont, zostały powymieniane \
wszystkie instalacje, umieszczono nowe wyposażenie -samo mieszkanie jest zadbane i nie wymaga żadnych nakładów finansowych.Powierzchnia wynosi 47,7m² \
i składa się z jasnego salonu z balkonem francuskim, drugiego pokoju i przedpokoju z pojemną szafą. Łazienka jest z wanna oraz osobnym WC, \
a kuchnia jest oddzielna oraz wyposażona w zmywarkę, piekarnik, lodówkę oraz płytę indukcyjną. Aktualny układ mieszkania pozwala na \
połączenie pomieszczeń w celu otwarcia większej przestrzeni oraz aranżacji według własnego stylu. W budynku jest winda. Pod budynkiem \
znajduje się wiele miejsc parkingowych dzięki czemu nigdy nie ma problemu z parkowaniem, a w pobliżu są również przystanki autobusowe \
dla osób niezmotoryzowanych. Sama okolica jest cicha i spokojna - idealna dla osób, które sobie cenią te atuty. Mieszkanie znajduje się \
na obrzeżach miasta, gdzie jest blisko do wylotówki na autostradę jednak dojazd do centrum Szczecina zajmuje 10/15 minut. Natomiast w \
pobliżu jest wiele punktów handlowych i usługowych m.in. galerie handlowe, restauracje, kino, sklepy czy plac zabaw. \
Jeśli pracujesz poza miastem i potrzebujesz mieszkania blisko obwodnicy lub szukasz czegoś z dala od miejskiego zgiełku ta \
oferta jest idealna dla Ciebie. Szczególnie polecam singlom czy parze bez dzieci. Serdecznie zapraszam do kontaktu w celu \
obejrzenia mieszkania.
"""

print(overall_chain({'real_estate_offer': offer_description, "offer_parameters": parameters}), end='\n')
