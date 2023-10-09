from src.gpt.chain.chaning import year_of_constr_chain, material_chain, building_type_chain, \
    number_floors_chain, balcony_summary_chain, balcony_rating_chain, \
    law_status_summary_chain, law_status_rating_chain, elevator_summary_chain, elevator_rating_chain, \
    basement_summary_chain, basement_rating_chain, garage_summary_chain, garage_rating_chain, garden_summary_chain, \
    garden_rating_chain, monitoring_summary_chain, monitoring_rating_chain, rent_summary_chain, rent_rating_chain, \
    outbuilding_summary_chain, outbuilding_rating_chain, kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain, technology_summary_chain, technology_rating_chain

main_chain = [
    year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
    technology_summary_chain, technology_rating_chain,
    balcony_summary_chain, balcony_rating_chain,
    law_status_summary_chain, law_status_rating_chain,
    elevator_summary_chain, elevator_rating_chain,
    basement_summary_chain, basement_rating_chain,
    garage_summary_chain, garage_rating_chain,
    garden_summary_chain, garden_rating_chain,
    monitoring_summary_chain, monitoring_rating_chain,
    rent_summary_chain, rent_rating_chain,
    outbuilding_summary_chain, outbuilding_rating_chain,
]

main_output_variables = [
    "balcony_summary", "balcony_rating",
    "technology_summary", "technology_rating",
    "law_summary", "law_rating",
    "elevator_summary", "elevator_rating",
    "basement_summary", "basement_rating",
    "garage_summary", "garage_rating",
    "garden_summary", "garden_rating",
    "monitoring_summary", "monitoring_rating",
    "rent_summary", "rent_rating",
    "outbuilding_summary", "outbuilding_rating",
]