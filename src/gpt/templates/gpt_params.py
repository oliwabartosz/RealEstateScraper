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
