from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

from src.gpt.model import llm
from src.gpt.templates import gpt_params, gpt_summaries, gpt_ratings


def create_llm_chain(llm_model, prompt: str, output_key: str):
    prompt = ChatPromptTemplate.from_template(prompt)
    return LLMChain(llm=llm_model, prompt=prompt, output_key=output_key)


# Chaining...

# PARAMETERS
# Year of the construction of the building
year_of_constr_chain = create_llm_chain(llm, gpt_params.year_of_constr_prompt, "year_of_constr")
# Building type
building_type_chain = create_llm_chain(llm, gpt_params.building_type_prompt, "building_type")
# Material of the building that have been constructed
material_chain = create_llm_chain(llm, gpt_params.material_prompt, "material")
# Number of floors that building have
number_floors_chain = create_llm_chain(llm, gpt_params.number_floors_prompt, "number_of_floors")

# SUMMARIES
# Technology
technology_summary_chain = create_llm_chain(llm, gpt_summaries.technology_prompt, "technology_summary")
# Law status
law_status_summary_chain = create_llm_chain(llm, gpt_summaries.law_status_prompt, "law_summary")
# Balcony
balcony_summary_chain = create_llm_chain(llm, gpt_summaries.balcony_prompt, "balcony_summary")
# Elevator
elevator_summary_chain = create_llm_chain(llm, gpt_summaries.elevator_prompt, "elevator_summary")
# Basement
basement_summary_chain = create_llm_chain(llm, gpt_summaries.basement_prompt, "basement_summary")
# Garage
garage_summary_chain = create_llm_chain(llm, gpt_summaries.garage_prompt, "garage_summary")
# Garden
garden_summary_chain = create_llm_chain(llm, gpt_summaries.garden_prompt, "garden_summary")
# Monitoring
monitoring_summary_chain = create_llm_chain(llm, gpt_summaries.monitoring_prompt, "monitoring_summary")
# Kitchen
kitchen_summary_chain = create_llm_chain(llm, gpt_summaries.kitchen_prompt, "kitchen_summary")
# Rent
rent_summary_chain = create_llm_chain(llm, gpt_summaries.rent_prompt, "rent_summary")
# Outbuilding
outbuilding_summary_chain = create_llm_chain(llm, gpt_summaries.outbuilding_prompt, "outbuilding_summary")
# Modernization
modernization_summary_chain = create_llm_chain(llm, gpt_summaries.modernization_prompt, "modernization_summary")


# RATINGS
# Technology
technology_rating_chain = create_llm_chain(llm, gpt_ratings.technology_prompt, "technology_rating")
# Law status
law_status_rating_chain = create_llm_chain(llm, gpt_ratings.law_status_prompt, "law_rating")
# Balcony
balcony_rating_chain = create_llm_chain(llm, gpt_ratings.balcony_prompt, "balcony_rating")
# Elevator
elevator_rating_chain = create_llm_chain(llm, gpt_ratings.elevator_prompt, "elevator_rating")
# Basement
basement_rating_chain = create_llm_chain(llm, gpt_ratings.basement_prompt, "basement_rating")
# Garage
garage_rating_chain = create_llm_chain(llm, gpt_ratings.garage_prompt, "garage_rating")
# Garden
garden_rating_chain = create_llm_chain(llm, gpt_ratings.garden_prompt, "garden_rating")
# Monitoring
monitoring_rating_chain = create_llm_chain(llm, gpt_ratings.monitoring_prompt, "monitoring_rating")
# Kitchen
kitchen_rating_chain = create_llm_chain(llm, gpt_ratings.kitchen_prompt, "kitchen_rating")
# Rent
rent_rating_chain = create_llm_chain(llm, gpt_ratings.rent_prompt, "rent_rating")
# Outbuilding
outbuilding_rating_chain = create_llm_chain(llm, gpt_ratings.outbuilding_prompt, "outbuilding_rating")
# Modernization
modernization_rating_chain = create_llm_chain(llm, gpt_ratings.modernization_prompt, "modernization_rating")
